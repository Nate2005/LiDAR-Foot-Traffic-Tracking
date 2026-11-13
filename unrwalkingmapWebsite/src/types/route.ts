export type TravelMode = 'walking' | 'bike'

export interface Building {
  id: string
  name: string
}

export interface RouteRequest {
  /** null means "use the user's current location" */
  fromId: string | null
  toId: string
  mode: TravelMode
  ada: boolean
}
