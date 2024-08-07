'''
Kelompok        : 1

Batch           : HCK - 017

Objective       : Program ini ditulis untuk membuat workflow task DAG. Program ini terdiri dari beberapa step seperti input data dari database, 
                  mengambil data dari database, membersihkan data, menyimpan data, membuat schedule daily batch processing, dan mendefinisikan alur task DAG

Catatan         : Setelah run, tolong tunggu hingga 1 menit agar dapat masuk ke laman login airflow
'''


from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine 
import pandas as pd
import uuid
from elasticsearch import Elasticsearch
import pendulum
 
# Membuat path data
raw_data_path_usedcar = '/opt/airflow/dags/usedcar_data_raw.csv' 
raw_data_path_faq = '/opt/airflow/dags/FAQ_data_raw.csv' 
fromPG_usedcar_path = '/opt/airflow/dags/usedcar__dataPG_raw.csv'
fromPG_faq_path = '/opt/airflow/dags/faq_dataPG_raw.csv'
clean_usedcar_path = '/opt/airflow/dags/clean_usedcar_data.csv'
clean_faq_path = '/opt/airflow/dags/clean_faq_data.csv'

# Membuat nama database, username, dan password postgre
database = "airflow_fp"
username = "airflow_fp"
password = "airflow_fp"
host = "postgres"

# Membuat variable koneksi postgre
postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

# Membuat koneksi sqlalchemy
engine = create_engine(postgres_url)
conn = engine.connect()

def load_csv_pg():

    '''
    Fungsi ini digunakan untuk melakukan data loading/input data ke server postgre.
    Cara kerja :
    1. Membuat dataframe dari alamat raw_data_path
    2. Load table 'table_used_car' dan 'table_faq' ke dalam server postgre
    '''

    # Membuat dataframe dataset usedcar dan FAQ
    df = pd.read_csv(raw_data_path_usedcar)
    df2 = pd.read_csv(raw_data_path_faq)

    # Konversi dataframe usedcar ke table sql
    df.to_sql('table_used_car', conn, index=False, if_exists='replace')  
    df2.to_sql('table_faq', conn, index=False, if_exists='replace')  


def take_data_postgre():

    '''
    Fungsi ini digunakan untuk mengambil data dari dari database 'airflow_m3' yang berada di server postgre.
    Cara kerja :
    1. Mengkoneksikan ke database airflow_fp
    2. Membuka 'table_m3' dari database airflow_fp
    3. Membuat dataframe dari 'table_used_car' dan 'table_faq'
    4. Menyimpan dataframe ke dalam format csv
    '''

    # Melakukan koneksi ke database dan membuat dataframe dari table_used_car dan table_faq
    df = pd.read_sql_query("select * from table_used_car", conn) 
    df2 = pd.read_sql_query("select * from table_faq", conn) 

    # Konversi dataframe ke format csv
    df.to_csv(fromPG_usedcar_path, sep=',', index=False)
    df2.to_csv(fromPG_faq_path, sep=',', index=False)

    
def data_cleaning():

    ''' 
    Fungsi ini digunakan untuk membersihkan data agar data siap dan dapat dipakai untuk analisa.
    Cara kerja :
    1. Loading data
    2. Menghapus karakter spasi pada bagian depan dan belakang kolom
    3. Mengubah format nama kolom menjadi format lowercase
    4. Mengganti karakter spasi pada kolom dengan karakter '_'
    5. Mengganti nama kolom pada dataframe usedcar
    6. Ubah nilai 0 dan 1 menjadi nilai yang sesuai dengan semantik
    7. Mengubah nilai kolom plate_type menjadi nilai yang relevan
    8. Buat kolom baru dari hasil kombinasi kolom - kolom lain pada dataset used car
    9. Menghapus baris duplikat pada dataset FAQ
    10. Menghapus beberapa karakter tertentu pada dataset FAQ
    11. Drop column yang tidak relevan pada dateset FAQ
    12. Menyimpan data hasil cleaning ke format csv
    '''

    # Load data
    df = pd.read_csv(fromPG_usedcar_path)
    df2 = pd.read_csv(fromPG_faq_path, index_col=0)

    # Mengubah format nama kolom menjadi format lowercase pada dataset usedcar
    df.columns = df.columns.str.lower()

    # Mengganti karakter spasi pada nama kolom dataset usedcar dengan karakter '_'
    df.columns = df.columns.str.replace(' ', '_')

    # Mengganti nama kolom pada dataframe usedcar
    df.rename(columns={'price_(rp)' : 'harga_(Rp)', 'instalment_(rp|monthly)' : 'cicilan_(Rp/month)', 'mileage_(km)' : 'jarak_tempuh(km)', 'car_name' : 'nama_mobil', 'year' : 'tahun_rilis', 'transmission' : 'transmisi'}, inplace=True)

    # Ubah nilai 0 dan 1 menjadi nilai yang sesuai dengan semantik
    for col in ['rear_camera', 'sun_roof', 'auto_retract_mirror', 'electric_parking_brake', 'map_navigator', 'vehicle_stability_control', 'keyless_push_start', 'sports_mode', '360_camera_view', 'power_sliding_door', 'auto_cruise_control'] :   
        df[col] = df[col].replace({0 : 'Tidak ada atau tidak memiliki', 1 : 'Ada atau memiliki'})
    
    # Mengubah nilai kolom plate_type menjadi nilai yang relevan
    df['plate_type'] = df['plate_type'].replace({'even plate' : 'Plat genap', 'odd plate' : 'Plat ganjil'})

    # Buat kolom baru hasil kombinasi kolom - kolom lain
    df['combined_info'] = df.apply(
        lambda row: (
            f"Nama mobil: {row['nama_mobil']}, "
            f"Brand mobil: {row['brand']}, "
            f"Tahun perilisan mobil: {row['tahun_rilis']}, "
            f"Jarak yang telah ditempuh (km): {row['jarak_tempuh(km)']}, "
            f"Lokasi penjual: {row['location']}, "
            f"Jenis transmisi: {row['transmisi']}, "
            f"Tipe plat nomor: {row['plate_type']}, "
            f"Rear camera: {row['rear_camera']}, "
            f"Sun roof: {row['sun_roof']}, "
            f"Spion otomatis: {row['auto_retract_mirror']}, "
            f"Electric parking brake: {row['electric_parking_brake']}, "
            f"Map navigator: {row['map_navigator']}, "
            f"Stability control: {row['vehicle_stability_control']}, "
            f"Push start: {row['keyless_push_start']}, "
            f"Sport mode: {row['sports_mode']}, "
            f"Kamera 360 derajat: {row['360_camera_view']}, "
            f"Sliding door: {row['power_sliding_door']}, "
            f"Cruise control: {row['auto_cruise_control']}, "
            f"Harga mobil (Rp): {row['harga_(Rp)']}, "
            f"Cicilan per bulan: {row['cicilan_(Rp/month)']}"
    ), axis=1
)

    # Menghapus baris duplikat pada dataset FAQ
    df2.drop_duplicates(inplace=True)

    # Menghapus beberapa karakter tertentu pada dataset FAQ
    df2['Answer'] = df2['Answer'].str.replace(r'\[|\]|\'|\"', '', regex=True)

    # Reset index
    df2.reset_index(inplace=True)

    # Drop column Unnamed
    df2.drop(columns='Unnamed: 0', inplace=True)

    # Menyimpan data hasil cleaning ke format csv
    df.to_csv(clean_usedcar_path, sep=',', index=False)
    df2.to_csv(clean_faq_path, sep=',', index=False)


def upload_Cleancsv_pg():

    '''
    Fungsi ini digunakan untuk melakukan data input data clean ke server postgre.
    Cara kerja :
    1. Load data CSV
    2. Load table 'table_used_car_clean' dan 'table_faq_clean' ke dalam server postgre
    '''

    # Membuat dataframe dataset usedcar dan FAQ
    df = pd.read_csv(clean_usedcar_path)
    df2 = pd.read_csv(clean_faq_path)

    # Konversi dataframe usedcar ke table sql
    df.to_sql('table_used_car_clean', conn, index=False, if_exists='replace')  
    df2.to_sql('table_faq_clean', conn, index=False, if_exists='replace')  
    

def upload_to_elasticsearch():

    '''
    Fungsi ini digunakan untuk mengupload data yang sudah bersih ke server elasticsearch.
    Cara kerja :
    1. Membuat object server elasticsearch
    2. Load data hasil cleaning
    3. Mengubah format data menjadi format dictionary agar dapat dibaca dengan json
    '''

    # Membuat object server
    es = Elasticsearch("http://elasticsearch:9200")

    # Membaca file hasil cleaning
    df = pd.read_csv(clean_usedcar_path, index_col=0)
    df2 = pd.read_csv(clean_faq_path, index_col=0)
    
    # Looping untuk mengconvert tiap row menjadi dictionary
    for i, r in df.iterrows():
        doc1 = r.to_dict()  
        res1 = es.index(index="table_usedcar", id=i+1, body=doc1)
        print(f"Response from Elasticsearch: {res1}")
    
    # Looping untuk mengconvert tiap row menjadi dictionary
    for i, r in df2.iterrows():
        doc2 = r.to_dict()  
        res2 = es.index(index="table_faq", id=i+1, body=doc2)
        print(f"Response from Elasticsearch: {res2}")

        
default_args = {
    'owner': 'Fp', 
    'start_date': datetime(2024, 7, 27, tzinfo=pendulum.timezone('Asia/Jakarta'))
}


with DAG(
    "FinalProject", 
    description='Final Project DAG',
    schedule_interval= '30 06 * * *', 
    default_args=default_args, 
    catchup=False
    ) as dag:
    
        # Task : 1
        '''Task ini ditujukan untuk melakukan load data ke server postgre'''
        load_csv_pg_task = PythonOperator(
            task_id='load_csv_pg',
            python_callable=load_csv_pg) 
    
        # Task: 2
        '''Task ini ditujukan untuk mengambil data dari database yang telah dibuat pada server postgre'''
        take_data_postgre_task = PythonOperator(
            task_id='take_data_postgre',
            python_callable=take_data_postgre) #
    

        # Task: 3
        '''Task ini ditujukan untuk melakukan proses cleaning pada data'''
        data_cleaning_task = PythonOperator(
            task_id= 'data_cleaning',
            python_callable= data_cleaning)
        
        # Task : 4
        '''Task ini ditujukan untuk melakukan input data clean ke server postgre'''
        load_Cleancsv_pg_task = PythonOperator(
            task_id='load_Cleancsv_pg',
            python_callable=upload_Cleancsv_pg) 

        # Task: 5
        '''Task ini ditujukan untuk mengupload data ke server elasticsearch'''
        upload_to_elastic_task = PythonOperator(
            task_id='upload_data_elastic',
            python_callable=upload_to_elasticsearch)

        # Urutan task
        load_csv_pg_task >> take_data_postgre_task >> data_cleaning_task >> load_Cleancsv_pg_task >> upload_to_elastic_task
