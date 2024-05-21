from abc import ABC
from segment import train as train_seg
from segment import predict as predict_seg
from tkinter import filedialog
import os


class Yolov9(ABC):

    def __init__(self, mode):
        self.mode = mode

        if self.mode in ['instance-segmentation']:
            self.model = Yolov9InstanceSegmentation(None)

    def train(self, **kwargs):
        return self.model.train(**kwargs)

    def predict(self, **kwargs):
        return self.model.predict(**kwargs)

class Yolov9InstanceSegmentation(Yolov9):

    def __init__(self, mode):
        super().__init__(mode)

    def train(self, **kwargs):

        data = kwargs.get('data', None)

        assert data is not None

        opt = train_seg.parse_opt()

        opt.data = data
        opt.epochs = kwargs.get('epochs', 1)

        opt.workers = kwargs.get('workers', 8)
        opt.device = kwargs.get('device', 0)
        opt.batch_size = kwargs.get('batch_size', 8)
        opt.imgsz = kwargs.get('imgsz', 640)
        opt.weights = kwargs.get('weights', '')
        opt.hyp = kwargs.get('hyp', 'hyp.scratch-high.yaml')
        opt.close_mosaic = kwargs.get('close_mosaic', 10)
        opt.no_overlap = kwargs.get('no_overlap', True)
        opt.project = kwargs.get('project', None)
        opt.cfg = kwargs.get('cfg', 'models/segment/gelan-c-seg.yaml')
        opt.name = kwargs.get('name', 'gelan-c-seg')

        train_seg.main(opt)

    def predict(self, **kwargs):
        source = kwargs.get('source', None)
        weights = kwargs.get('weights', None)

        assert source is not None
        assert weights is not None

        opt = predict_seg.parse_opt()

        opt.source = source
        opt.weights = weights   

        opt.imgsz = kwargs.get('imgsz', (640,640))
        opt.iou_thres = kwargs.get('iou_thres', 0.70)
        opt.conf_thres = kwargs.get('conf_thres', 0.70)
        opt.device = kwargs.get('device', 0)
        opt.name = kwargs.get('name', 'yolov9-seg')
        opt.hide_labels = kwargs.get('hide_labels', True)
        opt.hide_conf = kwargs.get('hide_conf', False)
        opt.save_txt = kwargs.get('save_txt', False)
        opt.exist_ok = kwargs.get('exist_ok', False)

        predict_seg.main(opt)
        output_dir = os.path.join(opt.project, opt.name, 'labels')
        return output_dir

def select_files():
    folder_path = filedialog.askdirectory(title="MR Görüntülerin Olduğu Dosyayı Seçin")
    return folder_path

if __name__ == "__main__":
    model = Yolov9('instance-segmentation')
    sources = select_files()
    sources = sources.replace("\\","/")
    #model.train(data='data.yaml', epochs=150, batch_size=8, hide_labels=True)
    model.predict(source=sources, weights='yolov9-main\\runs\\train-seg\\gelan-c-seg61\\weights\\best.pt', hide_conf=True, hide_labels=True, iou_thres=0.75, conf_thres=0.75, save_txt=True, exist_ok=True, project="detections", name="kidney", imgsz=(512,512))