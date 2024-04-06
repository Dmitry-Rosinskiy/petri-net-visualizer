// Информация о текущих масштабах изображения
const scaleInfo = {}
// Максимально допустимый масштаб изображения
const maxScale = 30;
// Минимально допустимый масштаб изображения
const minScale = -30;
// Коэффициент единичного изменения масштаба изображения
const scaleCoef = 1.1;
// Радиус области клика
const clickRadius = 20;

// Добавление события нажатия по изображению
const addClickEventToImage = (data) => {
    console.log(data);
    const elemImage = document.getElementById("visualization");
    // Если текущая страница не визуализация, событие не создаётся
    if (elemImage === null) {
        return;
    }

    elemImage.addEventListener("click", (event) => {
        onImageClick(event, data);
    })
}

// Обработчик нажатия по изображению
const onImageClick = (event, data) => {
    // Если визуализируется основной (иерархический) процесс
    if (isMainProcessSelected()) {
        for (const transition of Object.keys(data)) {
            // Если в область клика попадает один из переходов
            if (withinClickRadius(event.offsetX, event.offsetY, data[transition].x, data[transition].y, clickRadius)) {
                const elemSubprocessButton = document.getElementById(transition);
                if (elemSubprocessButton !== null) {
                    elemSubprocessButton.onclick.apply(elemSubprocessButton);
                    console.log(transition, data[transition].x, data[transition].y)
                }
            }
        }
        console.log("x =", event.offsetX, ", y =", event.offsetY);
    }
}

// Обработчик нажатия кнопки процесса
const clickProcessButton = (element) => {
    const elemImage = document.getElementById("visualization");
    const oldImage = elemImage.src;

    // Если масштаб старого изображения прежде не менялся (нет информации о нём), создаётся по умолчанию
    if (scaleInfo[oldImage] === undefined) {
        scaleInfo[oldImage] = 0;
    }

    // Меняется масштаб текущего изображения до значения по умолчанию, при этом само хранимое значение масштаба не изменяется
    changeImageScale(-scaleInfo[oldImage], false);

    const imageName = element.getAttribute("id");
    elemImage.src = "static/petri_net_images/" + imageName + ".png";
    const newImage = elemImage.src;

    // Если масштаб нового изображения прежде не менялся (нет информации о нём), создаётся по умолчанию
    if (scaleInfo[newImage] === undefined) {
        scaleInfo[newImage] = 0;
    }

    // Меняется масштаб текущего изображения до сохранённого значения, при этом само хранимое значение масштаба не изменяется
    changeImageScale(scaleInfo[newImage], false);

    const elemProcessCaption = document.getElementById("process-caption");
    elemProcessCaption.innerHTML = element.getAttribute("id");

    const processButtons = document.getElementsByClassName("selected-button")
    // Все кнопки, которые были выбраны (кнопка предыдущего процесса), становится доступной
    for (const processButton of processButtons) {
        processButton.classList.remove("selected-button");
        processButton.removeAttribute("disabled");
    }

    // Текущая нажатая кнопка становится недоступной
    element.classList.add("selected-button");
    element.setAttribute("disabled", "disabled");
}

// Показ процесса загрузки файлов
const showLoading = () => {
    const elemProcessFileInput = document.getElementById("process-file");
    const elemSubprocessFilesInput = document.getElementById("subprocess-files");
    // Если файл основного (иерархического) процесса или ни одного подпроцесса не были загружены
    if (elemProcessFileInput.files.length === 0 || elemSubprocessFilesInput.files.length === 0) {
        return;
    }

    // Показ состояния загрузки файлов
    const elemForm = document.getElementById("input-form");
    elemForm.setAttribute("hidden", "hidden");
    const elemLoadingBlock = document.getElementById("loading");
    elemLoadingBlock.removeAttribute("hidden");
}

// Перенаправление на страницу для загрузки архива
const redirectToDownloadPage = () => {
    location.href = "/download";
}

// Обработчик кнопки увеличения масштаба изображения
const zoomInImage = () => {
    const elemImage = document.getElementById("visualization");
    const imageName = elemImage.src;

    // Если масштаб изображения прежде не менялся (нет информации о нём), создаётся по умолчанию
    if (scaleInfo[imageName] === undefined) {
        scaleInfo[imageName] = 0;
    }

    // Если изображение можно увеличить (меньше максимально допустимого масштаба)
    if (scaleInfo[imageName] < maxScale) {
        // Увеличение масштаба изображения
        changeImageScale(1, true);
    }
}

// Обработчик кнопки уменьшения масштаба изображения
const zoomOutImage = () => {
    const elemImage = document.getElementById("visualization");
    const imageName = elemImage.src;

    // Если масштаб изображения прежде не менялся (нет информации о нём), создаётся по умолчанию
    if (scaleInfo[imageName] === undefined) {
        scaleInfo[imageName] = 0;
    }

    // Если изображение можно уменьшить (больше минимально допустимого масштаба)
    if (scaleInfo[imageName] > minScale) {
        // Уменьшение масштаба изображения
        changeImageScale(-1, true);
    }
}

// Изменение масштаба изображения
const changeImageScale = (value, changeCurrentScale) => {
    const elemImage = document.getElementById("visualization");

    // Если происходит увеличение масштаба
    if (value > 0) {
        for (let i = 0; i < value; i++) {
            // Умножение высоты изображения на определённый коэффицент
            elemImage.height = elemImage.height * scaleCoef;
        }
    // Если происходит уменьшение масштаба
    } else {
        for (let i = 0; i < -value; i++) {
            // Деление высоты изображения на определённый коэффицент
            elemImage.height = elemImage.height / scaleCoef;
        }
    }

    // Если необходимо поменять хранимое значение масштаба изображения
    if (changeCurrentScale) {
        const imageName = elemImage.src;
        scaleInfo[imageName] += value;
    }
}

// Проверяет, что точка клика находится в указанной области
const withinClickRadius = (clickX, clickY, centerX, centerY, radius) => {
    return (clickX >= centerX - radius && clickX <= centerX + radius) && (clickY >= centerY - radius && clickY <= centerY + radius);
}

// Проверяет, является ли текущий визуализируемый процесс основным (иерархическим)
const isMainProcessSelected = () => {
    const elemSelectedButton = document.getElementsByClassName("selected-button").item(0);
    return elemSelectedButton.classList.contains("process-button");
}