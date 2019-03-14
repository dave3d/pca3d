
pca.html:	axis.x3d frame.x3d output.x3d x3d2html.py
	./x3d2html.py -o pca.html -r 'XAXIS:PCo1' -r 'YAXIS:PCo2' -r 'ZAXIS:PCo3' -t "Dave's PCA X3d test" axis.x3d frame.x3d output.x3d

output.x3d:	pca2x3d.py pcoa_binomial.csv
	./pca2x3d.py -o output.x3d pcoa_binomial.csv

clean:
	rm output.x3d pca.html
