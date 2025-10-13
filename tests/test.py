import os
import uuid

from ultralytics import YOLO

def detection_video(path_to_video: str, path_to_model: str, save_path: str = "./detected_videos", show: bool = False, save_json: bool = True, save_text: bool = True, num_workers: int = None, verbose: bool = False) -> None:
    """
    Размечает видео
    :param path_to_video: Путь до видео.
    :param path_to_model: Путь до модели.
    :param save_path: Путь каталога котором будет сохранено видео, jsonl и text файлы
    :param show: Bool переменная, true если нужно отобразить видео, false иначе, по умолчанию false
    :param save_json: Bool переменная, true если нужно сохранить jsonl file, false иначе, по умолчанию false (сохранение как {save_path}/*.jsonl)
    :param save_text: Bool переменная, true если нужно сохранить text file, false иначе, по умолчанию false (сохранение как {save_path}/labels/*.txt)
    :param num_workers: Int переменная, можно вручную указать кол-во используемых ядер для обработки видео
    :param verbose: Bool переменная, true если нужно выводить логи обработки видео, false иначе, по умолчанию false
    :return: Ничего не возвращает
    """
    assert os.path.exists(path_to_video)
    assert os.path.exists(path_to_model)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    model = YOLO(path_to_model)

    uid = uuid.uuid4()

    file_name = "video-" + uid.__str__()

    results_dir = os.path.join(save_path, file_name)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    results = model.track(path_to_video, show=show, save=True, project=save_path, name=file_name, save_txt=save_text, stream=True, verbose=verbose)

    if save_json:
        with open(f"{save_path}/{file_name}/{file_name}.jsonl", 'w') as output_json:
            for result in results:
                output_json.write(result.to_json() + '\n')


if __name__ == '__main__':
    print(-2 % 3)



