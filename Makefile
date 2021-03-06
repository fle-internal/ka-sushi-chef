en: pex
	mkdir -p out/
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite en 0.16


es: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite es 0.16 --subtitlelang=es --interfacelang=es-ES --contentlang=es-ES


pt-BR: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite pt-BR 0.16 --videolang=pt-BR --contentlang=pt-BR


sw: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite sw 0.16 --videolang=sw --subtitlelang=sw


pt-PT: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite pt-PT 0.16 --videolang=pt-PT --contentlang=pt-PT


bn: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite bn 0.16


de: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite de 0.16


fr: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite fr 0.16


da: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite da 0.16


bg: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite bg 0.16


ka: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite ka 0.16


id: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite id 0.16


hi: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite hi 0.16


xh: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite xh 0.16


ta: pex
	PEX_MODULE=contentpacks ./makecontentpacks ka-lite ta 0.16


sdist:
	python setup.py sdist


pex: sdist
	pex --python=python3 -r requirements.txt -o makecontentpacks --disable-cache --no-wheel dist/content-pack-maker-`python setup.py --version`.tar.gz
