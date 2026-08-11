АНИМАЦИИ
========

Покадровые ленты и Lottie-файлы для персонажей, зон и интерфейса.

Формат:
  спрайт-лист  — WebP или PNG, кадры в один ряд
  Lottie       — JSON

ОЖИДАЕМЫЕ ИМЕНА
  anim_<объект>_<действие>.webp   спрайт-лист
  anim_<объект>_<действие>.json   описание кадров или Lottie

Примеры:
  anim_lumi_idle.webp   + anim_lumi_idle.json
  anim_portal_open.webp + anim_portal_open.json

Описание кадров:
  {"frames":16,"w":320,"h":400,"fps":24,"loop":true}

ПОДКЛЮЧЕНИЕ
ASSET_MANIFEST.animations в index.html.
