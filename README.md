# Chinese reminder

A Qt5 app useful for memorizing chinese words and sentences.

![](https://github.com/mattyonweb/chinese-reminder/blob/master/docs/screen.png)

## Installation

The package is not yet on Pypi. 

Assuming you are using linux, you can try it in a virtual environment by doing:

```shell
git clone https://github.com/mattyonweb/chinese-reminder.git
python -m venv chinese-reminder/venv
cd chinese-reminder
source venv/bin/activate  # activate.fish if using the fish shell 
pip install .
chinese-reminder
```

If there are no installed dictionary files, the default one will be used (see `examples` directory).

### Running on Windows

Analogous steps should be followed to install the source code on Windows.

Note that, while being functionally equivalent to Linux, for some reason the GUI looks uglier on Windows.

## Dictionary files

Dictionary files are TSV (Tab-Separated Values) files such as the one in the `examples` directory. 

On Linux, these files are stored in: `~/.local/share/chinese-reminder/V1`

On Windows, these files are stored in: `C:\Users\<insert-here-your-user>\AppData\Local\chinese-reminder\chinese-reminder\V1`.

The words dictionary is called `dictionary.tsv` and must look like this:

```
chinese	pinyin	translations	difficulty
木	mù	albero	1
一	yī	uno	0
不	bù	non	0
女	nǚ	femminile	0
  (...)
```

The sentences dictionary is called `sentences.tsv` and must look like this:

```
groupid	original	translated
1	Da dove vieni?	你是哪儿的人？
1	Da dove venite?	你们是哪儿的人？
1	Da dove viene il tuo insegnante?	你的老师是哪儿的人？
2	Di che nazionalità sei?	你是那国人？
```