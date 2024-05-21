import cv2
import os
import numpy as np
import uuid

# İmgelerin bulunduğu dosya dizinini belirt
image_dir = "yolov9-main/data/test/images/"

# İmgelerin IoU skorlarının depolanması için önceden yer aç
iou_scores = []

# .txt uzantılı etiketlerden bilgileri al
def read_labels(label_path, image_shape):
    labels = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip().split()
                class_index = int(data[0])
                coordinates = [float(val) for val in data[1:]]
                x_coords = [int(val * image_shape[1]) for val in coordinates[::2]]
                y_coords = [int(val * image_shape[0]) for val in coordinates[1::2]]
                points = np.zeros((len(x_coords), 1, 2), dtype=np.int32)
                for i in range(len(x_coords)):
                    points[i][0] = [x_coords[i], y_coords[i]]
                labels.append({'class_index': class_index, 'points': points})       
    else:
        print(f"File Doesn't Exist! --> {label_path}")
        iou_scores.append(0)
    return labels


# Alınan bilgilerden maske oluştur
def mask_from_labels(labels, image_shape):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    for label in labels:
        cv2.fillPoly(mask, [label['points']], color=(255, 255, 255)) # Maskeyi oluştur
    return mask

# IoU (Intersection over Unions) yöntemi ile çakışan alanlar ile bir doğruluk skoru oluştur
def calculate_iou(mask1, mask2):
    intersection = cv2.bitwise_and(gt_mask, pred_mask)
    union = cv2.bitwise_or(gt_mask, pred_mask)
    iou_score = np.sum(intersection) / np.sum(union)
    return iou_score


for image_filename in os.listdir(image_dir):
    # Kaydedilecek sonuç için benzersiz bir isim tanımla
    unique_id = str(uuid.uuid4())

    image_path = os.path.join(image_dir, image_filename)
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape
    
    data_filename = os.path.splitext(image_filename)[0] + '.txt'
    data_path = os.path.join(image_dir.replace('test/images', 'test/labels'), data_filename)
    pred_path = os.path.join(image_dir.replace('data/test/images', 'runs/predict-seg/yolov9-seg20/labels'), data_filename)
    data_path = data_path.replace("\\", "/")
    pred_path = pred_path.replace("\\", '/')

    gt_labels = read_labels(data_path, (image_height, image_width))
    pred_labels = read_labels(pred_path, (image_height, image_width))
    
    # Maskeleri oluştur
    gt_mask = mask_from_labels(gt_labels, (image_height, image_width))
    pred_mask = mask_from_labels(pred_labels, (image_height, image_width))
    
    # IoU'yu hesapla
    iou_score = calculate_iou(gt_mask, pred_mask)
    iou_scores.append(iou_score)
    iou_mean = np.mean(iou_scores)

    for label in gt_labels:
        points = label['points']
        cv2.polylines(image, [points], isClosed=True, color=(0,255,0), thickness=2)
        cv2.fillPoly(image, [points], color=(0,255,0))

    for label in pred_labels:
        points = label['points']
        cv2.polylines(image, [points], isClosed=True, color=(0,0,255), thickness=2)
        cv2.fillPoly(image, [points], color=(0,0,255))
    
    # Sonucu kaydetmek için bir dizin oluştur
    output_image_folder = image_dir.replace('data/test/images', 'data/outputs/Images')
    output_image_path = os.path.join(output_image_folder, f"{unique_id}.jpg")
    output_mask_folder = output_image_folder.replace('data/outputs/Images', 'data/outputs/Masks')
    output_mask_path = os.path.join(output_mask_folder, f"{unique_id}.jpg")


    # Sonuçları kaydet ve göster
    cv2.imwrite(output_image_path, image)
    cv2.imwrite(output_mask_path, pred_mask)  
    cv2.putText(image, f"IoU: {iou_score:.4f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)     
    #cv2.imshow('Image with Polygons', image)


# Ortalama IoU Skorunu göster
print(f"The IoU Score Mean: {iou_mean:.4f}")
cv2.waitKey(0)
cv2.destroyAllWindows()