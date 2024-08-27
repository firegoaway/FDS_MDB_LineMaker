# MDBL - FDS MISC/DEVC/BNDF LINE MAKER

> Язык: **Python**

> Интерфейс: **Tkinter**

## Особенности и описание работы утилиты
Утилита позволяет добавить дополнительные измерители, в частности, **измерители теплового потока**, в вашу пожарную модель **FDS**.
Более того, поскольку ни одна программа, работающая с **FDS** на российском рынке не умеет определять необходимость переключения на тот или иной доступный в **FDS** метод вычисления, утилита сама высчитывает размер ячейки и автоматически переключает метож вычисления на ***VLES*** или ***LES***.

### Отличие VLES от LES
Выбор между **LES** (Large-Eddy Simulation) и **VLES** (Very Large-Eddy Simulation) может зависеть от конкретных требований задачи и доступности вычислительных ресурсов.

***VLES*** — это метод моделирования на больших сетках (размер ячейки от 0.2 м до 2 м). Под ***VLES*** вообще понимается довольно широкий круг подходов к решению задач гидрогазодинамики, от URANS до LES. В большинстве случаев он позволяет лишь воспроизвести общую картину исследуемого пожара и не приводит к достаточно точному предсказанию гидрогазодинамических характеристик.

_***LES***_ — это метод моделирования на средних и мелкомасштабных сетках (размер ячейки от 0.1 м до 0.4 м). Он разрешает только те структуры, размеры которых не ниже размеров ячеек расчётной сетки. Мелкомасштабная (подсеточная) турбулентность описывается с помощью модели подсеточной вязкости, тем самым обеспечивая возможность моделировать прогрев твёрдых тел (стен и иных конструкций), учитывая температуру в твёрдой фазе, а также позволяет моделировать пиролиз.

При переходе от размера ячейки 0.85 м или 0.425 м к размеру 0.2125 м имеет смысл переключить метод моделирования на **LES** для получения более точных результатов.

### Поддерживаемые версии FDS
> [**FDS 6.9.1**](https://github.com/firemodels/fds/releases/tag/FDS-6.9.1)
> [**FDS 6.9.0**](https://github.com/firemodels/fds/releases/tag/FDS-6.9.0)
> [**FDS 6.8.0**](https://github.com/firemodels/fds/releases/tag/FDS-6.8.0)

## Как установить и пользоваться

|	№ п/п	|	Действие	|
|---------|---------|
|	1	|	Скачайте последнюю версию **ZmejkaFDS** в разделе [**Releases**](https://github.com/firegoaway/Zmejka/releases)	|
|	2	|	Запустите **ZmejkaFDS.exe**. Нажмите **"Выбрать .fds"** и выберите файл сценария FDS	|
|	3	|	Во вкладке **"Параметры"** нажмите **"MDBL"**. Откроются новое окно	|
|	4	|	В окне **FDS MISC/DEVC/BNDF Line Maker** следуйте всплывающим подсказкам. Нажмите на кнопку **Добавить**, и утилита сохранит изменения в вашем файле сценария **".fds"**	|
|	5	|	Готово! Файл сценария **.fds** готов к запуску	|

> **MDBL** работает как самостоятельно, так и в связке с утилитой [**Zmejka**](https://github.com/firegoaway/Zmejka)

## Статус разработки
> **Альфа**

## Профилактика вирусов и угроз
- Утилита **"MDBL"** предоставляется **"как есть"**.
- Актуальная версия утилиты доступна в разделе [**Releases**](https://github.com/firegoaway/FDS_MDB_LineMaker/releases), однако использовать утилиту в отрыве от [**ZmejkaFDS**](https://github.com/firegoaway/Zmejka) не рекомендуется.
- Файлы, каким-либо образом полученные не из текущего репозитория, несут потенциальную угрозу вашему ПК.
- Файл с расширением **.exe**, полученный из данного репозитория, имеет уникальную Хэш-сумму, позволяющую отличить оригинальную утилиту от подделки.
- Хэш-сумма обновляется только при обновлении версии утилиты и всегда доступна в конце файла **README.md**.

### Актуальные Хэш-суммы
> MDBL.exe - **c97c0fe122947043e0ba81615b028f2b**