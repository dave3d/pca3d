
pca.html:	axis.x3d frame.x3d pca_plot.x3d x3d2html.py
	./x3d2html.py -o pca.html -r 'XAXIS:PCo1' -r 'YAXIS:PCo2' -r 'ZAXIS:PCo3' -t "Dave's PCA X3d test" axis.x3d frame.x3d pca_plot.x3d

pca_plot.x3d:	pca2x3d.py pcoa_binomial.csv
	./pca2x3d.py -o pca_plot.x3d pcoa_binomial.csv

pca.x3d:	axis.x3d pca_plot_nolabels.x3d x3d2html.py
	./x3d2html.py -x -o pca.x3d -r 'XAXIS:PCo1' -r 'YAXIS:PCo2' -r 'ZAXIS:PCo3' -t "Dave's PCA X3d test" axis.x3d pca_plot_nolabels.x3d

pca_plot_nolabels.x3d:	pca2x3d.py pcoa_binomial.csv
	./pca2x3d.py -t -o pca_plot_nolabels.x3d pcoa_binomial.csv

clean:
	rm -f output.x3d pca.html pca_plot.x3d pca_plot_nolabels.x3d
