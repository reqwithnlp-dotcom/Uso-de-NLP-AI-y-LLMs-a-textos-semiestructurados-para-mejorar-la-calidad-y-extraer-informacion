# WebDocumentacion

Sitio estático para consultar la documentación de los servicios del proyecto de investigación. Está construido con Vite, React, TypeScript, React Router y React Markdown.

## Ejecutar

```bash
npm install
npm run dev
```

Para generar la versión estática:

```bash
npm run build
npm run preview
```

## Cómo agregar un nuevo servicio

1. Crea una carpeta en `public/content/<id>/`, usando un slug único como `clasificador-entidades`.
2. Coloca dentro de esa carpeta el archivo `README.md` con la documentación del servicio.
3. Coloca en la misma carpeta las imágenes referenciadas desde el Markdown. Usa rutas relativas, por ejemplo `ejemplo.png`.
4. Agrega una única entrada en `src/services/services.config.ts`:

```ts
{
  id: 'clasificador-entidades',
  name: 'API Clasificación de Entidades',
  shortDescription: 'Identifica entidades relevantes dentro de un texto.',
  markdownPath: '/content/clasificador-entidades/README.md',
}
```

El Home, el sidebar y la ruta `/servicio/<id>` se generan automáticamente a partir de ese array. No es necesario editar ningún otro componente.
