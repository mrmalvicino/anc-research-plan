# Evaluación subjetiva de la cancelación activa de ruido en auriculares

## Introducción

&nbsp;
Plan de investigación para la evaluación subjetiva de la cancelación activa de ruido en auriculares mediante análisis estadístico realizado con el módulo SciPy.

## Descargar PDF

&nbsp;
Cada vez que se realiza un cambio, una nueva versión del documento es compilada y publicada en [Releases](https://github.com/mrmalvicino/anc-research-plan/releases) y puede ser descargada libremente.

&nbsp;
Cabe aclarar que el compilador TexPDF no admite el paquete `fontspec` para usar Times New Roman. Para que funcione la automatización, este paquete está comentado en [packages.tex](./latex/include/packages.tex) y en su lugar se está usando `mathptmx`:

```latex
% \usepackage{fontspec} % Define \setmainfont{Times New Roman} (requiere LuaLatex)
%     \setmainfont{Times New Roman} % Documento con Times New Roman (requiere LuaLatex)

\usepackage{mathptmx}  % Documento con simil Times New Roman (compila con TexPDF)
```

&nbsp;
Una alternativa para poder complir con un formato que use esa tipografía es compilar localmente con MikTex o usar el compilador LuaLatex con Overleaf, para lo que habría que comentar `\usepackage{mathptmx}` y descomentar `\usepackage{fontspec}` y `\setmainfont{Times New Roman}`.

## Licencia y contribuciones

&nbsp;
Este proyecto de código abierto está disponible conforme a los términos de la [licencia MIT](./LICENSE).

&nbsp;
¡Las contribuciones son bienvenidas!
Si encontrás algún error, por más mínimo que sea, no dudes en abrir un [issue](https://github.com/mrmalvicino/anc-research-plan/issues/) para hacérmelo saber.
También podés hacer un fork y un pull request para incorporar la corrección por tu cuenta.