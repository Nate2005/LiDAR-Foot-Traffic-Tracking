import type { Building } from '../types/route'

// Temporary static list until GET /api/buildings (ApiController.getBuildings) exists.
// Names should be double-checked against the Wolf Pack Map.
export const buildings: Building[] = [
  { id: 'pennington-engineering', name: 'William Pennington Engineering Building' },
  { id: 'joe-crowley-union', name: 'Joe Crowley Student Union' },
  { id: 'knowledge-center', name: 'Mathewson-IGT Knowledge Center' },
  { id: 'davidson-math-science', name: 'Davidson Mathematics and Science Center' },
  { id: 'ansari-business', name: 'Ansari Business Building' },
  { id: 'lawlor-events-center', name: 'Lawlor Events Center' },
  { id: 'mackay-stadium', name: 'Mackay Stadium' },
  { id: 'church-fine-arts', name: 'Church Fine Arts' },
  { id: 'scrugham-engineering', name: 'Scrugham Engineering-Mines' },
  { id: 'fleischmann-agriculture', name: 'Fleischmann Agriculture' },
]
