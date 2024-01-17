
echo rm originals/question-$1.tex
rm originals/question-$1.tex

echo rm texs/question-$1.tex
rm texs/question-$1.tex

echo python prepare-latex-files.py
python prepare-latex-files.py

echo cp originals/question-$1.tex texs/question-$1.tex
cp originals/question-$1.tex texs/question-$1.tex

echo python compile-pdfs.py
python compile-pdfs.py
