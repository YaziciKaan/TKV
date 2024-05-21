# TKV Projesi

Bu proje, YoloV9 kullanılarak girilen hastaların böbrek MR'ları üzerinden toplam hacim tahmini yapmayı amaçlamaktadır.

## Gereksinimler
requirements.txt dosyasında gerekli gereksinimler mevcuttur. Python 3.8.x versiyonunda projenin çalıştırılması önerilir.(Terminal Üzerinde)

## Kurulum

1. Projenin klonlanması:
    ```sh
    git clone https://github.com/YaziciKaan/TKV.git
    cd TKV
    ```

2. Sanal ortamın oluşturulması:
    ```sh
    py -3.8 -m venv my_venv
    ```

3. Sanal ortamı etkinleştirmek:
    - Windows:
        ```sh
        myenv\Scripts\activate
        ```

4. Gereksinimlerin kurulumu:
    ```sh
    pip install -r requirements.txt
    ```
## Kullanım

1. Projenin çalıştırılması:
    ```sh
    python totalkidneyvolume.py
    ```

2. Proje çalıştığında, dosyalarınızı seçmek için bir dosya seçici açılacaktır. Tahminler ve toplam böbrek hacmi hesaplanacaktır.

## Parametreler

Projede kullanılan bazı önemli parametreler:

- **Kesit Aralığı**: Görüntüler arasındaki kesit aralığı.
- **Kesit Kalınlığı**: Görüntülerin kesit kalınlığı.
