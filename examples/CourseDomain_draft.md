---
module: "CourseDomain"
preview-generated-at: "2026-03-20T12:00:00Z"
review-mode: incremental
generation-strategy: section-scoped
passes-completed: 1,2A,2B,3,4,5,6,7
---

# CourseDomain Draft

## Module Files
| File | Role |
|---|---|
| src/Controllers/CoursesController.cs | API controller |
| src/Services/CourseService.cs | Domain service |
| src/Repositories/EfCourseRepository.cs | Data access |

## Operations Map
| Operation | Handler |
|---|---|
| GET /courses | CoursesController.GetAll |
| POST /courses | CoursesController.Create |

## Architecture Overview
Controller -> Service -> Repository -> Database.

## Business Rules
| Rule | Why It Exists | Since When |
|---|---|---|
| Course codes are unique | Prevent duplicate catalog entries | v1.0 |

## Data Operations
| Type | Description |
|---|---|
| Read | Query course list and details |
| Write | Insert and update course records |
