# TKV Projesi

Bu proje, verilen hasta böbrek MR'ları üzerinden toplam hacim tahmini yapmayı amaçlamaktadır.

## Gereksinimler
yolov9-main klasörü içerisindeki requirements.txt dosyası ile gereksinimler yüklenmektedir.(Python 3.8.x sürümü kullanılması önerilir.)

## Kurulum

1. Projeyi klonlayın:
    ```sh
    git clone https://github.com/YaziciKaan/TKV.git
    cd TKV
    ```

2. Sanal ortam oluşturun:
    ```sh
    py -3.8 -m venv my_venv
    ```

3. Sanal ortamı etkinleştirin:
    - Windows:
        ```sh
        myenv\Scripts\activate
        ```

4. Gerekli paketleri yükleyin:
    ```sh
    pip install -r requirements.txt
    ```
## Kullanım

1. Projeyi çalıştırın:
    ```sh
    python totalkidneyvolume.py
    ```

2. Proje çalıştığında, dosyalarınızı seçmek için bir dosya seçici açılacaktır. Tahminler ve toplam böbrek hacmi hesaplanacaktır.

## Parametreler

Projede kullanılan bazı önemli parametreler:

- **Kesit Aralığı**: Görüntüler arasındaki kesit aralığı.
- **Kesit Kalınlığı**: Görüntülerin kesit kalınlığı.
