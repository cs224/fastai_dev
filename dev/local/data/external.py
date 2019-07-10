#AUTOGENERATED! DO NOT EDIT! File to edit: dev/04_data_external.ipynb (unless otherwise specified).

__all__ = ['download_url', 'URLs', 'get_path', 'ConfigKey', 'download_data', 'untar_data']

from ..imports import *
from ..test import *
from ..core import *

def download_url(url, dest, overwrite=False, pbar=None, show_progress=True, chunk_size=1024*1024,
                 timeout=4, retries=5):
    "Download `url` to `dest` unless it exists and not `overwrite`"
    if os.path.exists(dest) and not overwrite: return

    s = requests.Session()
    s.mount('http://',requests.adapters.HTTPAdapter(max_retries=retries))
    u = s.get(url, stream=True, timeout=timeout)
    try: file_size = int(u.headers["Content-Length"])
    except: show_progress = False

    with open(dest, 'wb') as f:
        nbytes = 0
        if show_progress:
            pbar = progress_bar(range(file_size), auto_update=False, leave=False, parent=pbar)
        try:
            for chunk in u.iter_content(chunk_size=chunk_size):
                nbytes += len(chunk)
                if show_progress: pbar.update(nbytes)
                f.write(chunk)
        except requests.exceptions.ConnectionError as e:
            fname = url.split('/')[-1]
            from fastai.datasets import Config
            data_dir = dest.parent
            print(f'\n Download of {url} has failed after {retries} retries\n'
                  f' Fix the download manually:\n'
                  f'$ mkdir -p {data_dir}\n'
                  f'$ cd {data_dir}\n'
                  f'$ wget -c {url}\n'
                  f'$ tar -zxvf {fname}\n'
                  f' And re-run your code once the download is successful\n')

class URLs():
    "Global constants for dataset and model URLs."
    LOCAL_PATH = Path.cwd()
    URL = 'http://files.fast.ai/data/examples/'
    MDL = 'http://files.fast.ai/models/'
    S3 = 'https://s3.amazonaws.com/fast-ai-'

    S3_IMAGE    = f'{S3}imageclas/'
    S3_IMAGELOC = f'{S3}imagelocal/'
    S3_NLP      = f'{S3}nlp/'
    S3_COCO     = f'{S3}coco/'
    S3_MODEL    = f'{S3}modelzoo/'

    # main datasets
    ADULT_SAMPLE        = f'{URL}adult_sample.tgz'
    BIWI_SAMPLE         = f'{URL}biwi_sample.tgz'
    CIFAR               = f'{URL}cifar10.tgz'
    COCO_SAMPLE         = f'{S3_COCO}coco_sample.tgz'
    COCO_TINY           = f'{URL}coco_tiny.tgz'
    HUMAN_NUMBERS       = f'{URL}human_numbers.tgz'
    IMDB                = f'{S3_NLP}imdb.tgz'
    IMDB_SAMPLE         = f'{URL}imdb_sample.tgz'
    ML_SAMPLE           = f'{URL}movie_lens_sample.tgz'
    MNIST_SAMPLE        = f'{URL}mnist_sample.tgz'
    MNIST_TINY          = f'{URL}mnist_tiny.tgz'
    MNIST_VAR_SIZE_TINY = f'{S3_IMAGE}mnist_var_size_tiny.tgz'
    PLANET_SAMPLE       = f'{URL}planet_sample.tgz'
    PLANET_TINY         = f'{URL}planet_tiny.tgz'
    IMAGENETTE          = f'{S3_IMAGE}imagenette.tgz'
    IMAGENETTE_160      = f'{S3_IMAGE}imagenette-160.tgz'
    IMAGENETTE_320      = f'{S3_IMAGE}imagenette-320.tgz'
    IMAGEWOOF           = f'{S3_IMAGE}imagewoof.tgz'
    IMAGEWOOF_160       = f'{S3_IMAGE}imagewoof-160.tgz'
    IMAGEWOOF_320       = f'{S3_IMAGE}imagewoof-320.tgz'

    # kaggle competitions download dogs-vs-cats -p {DOGS.absolute()}
    DOGS = f'{URL}dogscats.tgz'

    # image classification datasets
    CALTECH_101  = f'{S3_IMAGE}caltech_101.tgz'
    CARS         = f'{S3_IMAGE}stanford-cars.tgz'
    CIFAR_100    = f'{S3_IMAGE}cifar100.tgz'
    CUB_200_2011 = f'{S3_IMAGE}CUB_200_2011.tgz'
    FLOWERS      = f'{S3_IMAGE}oxford-102-flowers.tgz'
    FOOD         = f'{S3_IMAGE}food-101.tgz'
    MNIST        = f'{S3_IMAGE}mnist_png.tgz'
    PETS         = f'{S3_IMAGE}oxford-iiit-pet.tgz'

    # NLP datasets
    AG_NEWS                 = f'{S3_NLP}ag_news_csv.tgz'
    AMAZON_REVIEWS          = f'{S3_NLP}amazon_review_full_csv.tgz'
    AMAZON_REVIEWS_POLARITY = f'{S3_NLP}amazon_review_polarity_csv.tgz'
    DBPEDIA                 = f'{S3_NLP}dbpedia_csv.tgz'
    MT_ENG_FRA              = f'{S3_NLP}giga-fren.tgz'
    SOGOU_NEWS              = f'{S3_NLP}sogou_news_csv.tgz'
    WIKITEXT                = f'{S3_NLP}wikitext-103.tgz'
    WIKITEXT_TINY           = f'{S3_NLP}wikitext-2.tgz'
    YAHOO_ANSWERS           = f'{S3_NLP}yahoo_answers_csv.tgz'
    YELP_REVIEWS            = f'{S3_NLP}yelp_review_full_csv.tgz'
    YELP_REVIEWS_POLARITY   = f'{S3_NLP}yelp_review_polarity_csv.tgz'

    # Image localization datasets
    BIWI_HEAD_POSE     = f"{S3_IMAGELOC}biwi_head_pose.tgz"
    CAMVID             = f'{S3_IMAGELOC}camvid.tgz'
    CAMVID_TINY        = f'{URL}camvid_tiny.tgz'
    LSUN_BEDROOMS      = f'{S3_IMAGE}bedroom.tgz'
    PASCAL_2007        = f'{S3_IMAGELOC}pascal_2007.tgz'
    PASCAL_2012        = f'{S3_IMAGELOC}pascal_2012.tgz'

    #Pretrained models
    OPENAI_TRANSFORMER = f'{S3_MODEL}transformer.tgz'
    WT103              = f'{S3_MODEL}wt103.tgz'
    #TODO: remove this last one and make sure the mosr recent is up
    WT103_1            = f'{S3_MODEL}wt103-1.tgz'

def _get_config():
    config_path = Path(os.getenv('FASTAI_HOME', '~/.fastai')).expanduser()
    config_file = config_path/'config.yml'
    if config_file.exists():
        with open(config_file, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            if 'version' in config and config['version'] == 1: return config
    else: config = {}
    #File inexistent or wrong version -> going to default
    config = {'data_path':    str(config_path/'data'),
              'archive_path': str(config_path/'archive'),
              'model_path':   str(config_path/'models'),
              'version':      1}
    with open(config_file, 'w') as yaml_file:
        yaml.dump(config, yaml_file, default_flow_style=False)
    return config

ConfigKey = Enum('ConfigKey', 'Data Archive Model')

def get_path(c_key=ConfigKey.Data):
    return Path(_get_config()[f"{c_key.name.lower()}_path"])

def _url2path(url, c_key=ConfigKey.Archive):
    fname = url.split('/')[-1]
    local_path = URLs.LOCAL_PATH/('models' if c_key==ConfigKey.Model else 'data')/fname
    if local_path.exists(): return local_path
    return get_path(c_key)/fname

def download_data(url, fname=None, c_key=ConfigKey.Archive, force_download=False):
    "Download `url` to `fname`."
    fname = Path(fname or _url2path(url, c_key=c_key))
    fname.parent.mkdir(parents=True, exist_ok=True)
    if not fname.exists() or force_download:
        print(f'Downloading {url}')
        download_url(url, fname, overwrite=force_download)
    return fname

def _get_check(url):
    checks = json.load(open(Path(__file__).parent/'checks.txt', 'r'))
    return checks.get(url, None)

def _check_file(fname):
    size = os.path.getsize(fname)
    with open(fname, "rb") as f:
        hash_nb = hashlib.md5(f.read(2**20)).hexdigest()
    return [size,hash_nb]

def _add_check(url, fname):
    "Internal function to update the internal check file with `url` and check on `fname`."
    checks = json.load(open(Path(__file__).parent/'checks.txt', 'r'))
    checks[url] = _check_file(fname)
    json.dump(checks, open(Path(__file__).parent/'checks.txt', 'w'), indent=2)

def untar_data(url, fname=None, dest=None, c_key=ConfigKey.Data, force_download=False):
    "Download `url` to `fname` if `dest` doesn't exist, and un-tgz to folder `dest`."
    default_dest = _url2path(url, c_key=c_key).with_suffix('')
    dest = default_dest if dest is None else Path(dest)/default_dest.name
    fname = Path(fname or _url2path(url))
    if fname.exists() and _get_check(url) and _check_file(fname) != _get_check(url):
        print("A new version of this is available, downloading...")
        force_download = True
    if force_download:
        if fname.exists(): os.remove(fname)
        if dest.exists(): shutil.rmtree(dest)
    if not dest.exists():
        fname = download_data(url, fname=fname, c_key=c_key)
        if _get_check(url) and _check_file(fname) != _get_check(url):
            print(f"File downloaded is broken. Remove {fname} and try again.")
        tarfile.open(fname, 'r:gz').extractall(dest.parent)
    return dest