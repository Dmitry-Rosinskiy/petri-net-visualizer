from pm4py import read_pnml, save_vis_petri_net
from lxml import etree


# Сохранение изображения сети Петри, заданной с помощью файла .pnml
def save_image(pnml_file, file_name, directory, data, errors, is_main=True):
    data.clear()
    try:
        # Создание модели сети Петри на основании файла
        net, initial_marking, final_marking = read_pnml(pnml_file)
        for transition in net.transitions:
            label = transition.properties.get("trans_name_tag")
            graphics = transition.properties.get("layout_information_petri")
            if label is not None and graphics is not None:
                coords = {"x": graphics[0][0], "y": graphics[0][1]}
                data.setdefault(label, coords)

        # Конвертирование модели в изображение формата .png
        save_vis_petri_net(net, initial_marking, final_marking, directory + file_name + ".png")
    # Ошибка формата данных
    except etree.XMLSyntaxError as e:
        print(e)
        errors.append(f"Файл с {'основным ' if is_main else 'под'}процессом {file_name}.pnml имеет неверный формат.")
        # Неудачное сохранение
        return False
    # Другая ошибка
    except Exception as e:
        print(e)
        errors.append("Произошла проблема во время загрузки файлов. Подробности " + str(e))
        # Неудачное сохранение
        return False

    # Удачное сохранение
    return True
