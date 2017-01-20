ovitos ../plot_3d.py high_persistence.xyz $1 high_persistence.png
ovitos ../plot_3d.py low_persistence.xyz $1 low_persistence.png
ovitos ../plot_3d.py high_threshold.xyz $1 high_threshold.png
ovitos ../plot_3d.py ../models/sio2_porous.xyz $1 sio_porous.png
ovitos ../plot_3d.py best_fit_to_sio2.xyz $1 bestfit.png
montage low_persistence.png high_persistence.png high_threshold.png  -tile 3x1 -geometry +0+0 model_examples.png
cp model_examples.png /Users/nicolaasgroeneboom/work/papers/nanopores-paper
cp bestfit.png /Users/nicolaasgroeneboom/work/papers/nanopores-paper/model_test.png
cp sio_porous.png /Users/nicolaasgroeneboom/work/papers/nanopores-paper
