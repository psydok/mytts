import yaml
from pathlib import Path
from typing import Union, List, Any, Dict

out_path = Path('static/wavs')


def get_files(path: Union[str, Path], extension='.TextGrid') -> List[Path]:
    if isinstance(path, str): path = Path(path).expanduser().resolve()
    return list(path.rglob(f'*{extension}'))


def read_yaml(path: str) -> Dict[str, Any]:
    with open(path, 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    return config


def save_yaml(config: Dict[str, Any], path: str) -> None:
    with open(path, 'w+', encoding='utf-8') as stream:
        yaml.dump(config, stream, default_flow_style=False)
