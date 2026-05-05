# Engineering Decisions

## Why async processing?
Video generation is slow and non-blocking by nature.

## Why slide-based video?
Reduces complexity while maintaining educational value.

## Why local storage?
Avoids cloud overhead for prototype scope.

## Why FastAPI BackgroundTasks?
Simple, sufficient, avoids overengineering with Celery.