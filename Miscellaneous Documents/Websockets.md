# Standards for communicating

All messages sent over the websocket should use JSON. Each message should include a `type`, and each type will have its own set of keys that can accompany a message in that type. The protocol will differentiate between messages that are sent to and from the server.

## Messages to the server

### Type 1

Type 1 messages are exclusively reserved for game board updates.
`game_state` represents the board using the standard format
`turn` is an array like [0, 0], which represents the index in the outer and inner array of the piece placed

## Messages to the client

### Type 1

Type 1 messages are excusively used to communicate the state of the game itself. Sent on initial game start, reconnection and after every move.
`game_state` represents the game board using the standard format
`turn` represents the color of the player whose turn it is (either "B" or "W")
`color` represents the color of the player (either "B" or "W")

### Type 2

Type 2 messages communicate things related to the game that are not the board itself.

`event` specifies the event that happened

-    A value of `invalid_move` indicates that the move sent by this client was not valid
-    A value of `game_finished` indicates that the game is over (expects data)
-    A value of `placement_failure` indicates that the move sent by this client was not accepted

`data` any additional data that's required goes in here

-    If the event is `game_finished`, either `outcome` or `winner` must be set within `data`
     -    `outcome` if applicable, can indicate that the game was forfeited (or that a similar non-win outcome occurred)
     -    `winner` if applicable, is set to either "B" or "W"
