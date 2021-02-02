//  Copyright (c) Facebook, Inc. and its affiliates.
//  All rights reserved.
//
//  This source code is licensed under the license found in the
//  LICENSE file in the root directory of this source tree.

const state = {
  discarded: ["G5"],
  hands: {
    self: [
      { hints: ["Y", "1"] },
      { hints: ["Y"] },
      { hints: ["2"] },
      { hints: ["2"] },
      { hints: [] }
    ],
    player1: [
      { card: "Y5", hints: ["Y", "1"] },
      { card: "W2", hints: ["W"] },
      { card: "R2", hints: ["2"] },
      { card: "G2", hints: ["2"] },
      { card: "B5", hints: [] }
    ]
  },
  placed: {
    white: 0,
    red: 0,
    blue: 0,
    yellow: 0,
    green: 0
  },
  hintsLog: [],
  defuseCounter: 3,
  hintCounter: 8,
  cardsLeft: 30
};

export { state, convertState };

function convertCard(card) {
  try {
    const [value, color] = card.toUpperCase().split("");
    return color + value;
  } catch {
    console.log(`ERROR converting: ${card}`);
  }
}

function convertState(schema) {
  console.log("This is schema : ", schema);
  schema.otherBots = [];
  if (!schema.isConnected) return {};
  return {
    isPlayerTurn: true,
    discarded: schema.discards.map(convertCard),

    
    //hands: {
    //  self: new Array(5).fill(1).map((_, idx) => ({
    //    id: ["40","43","42","41","40"],
    //    card: convertCard(schema.cheatMyCards),
    //    hints: [[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]
    //  })),
    //  ["player" + schema.partnerId]: schema.cards.map((card, idx) => ({
    //    id: ["49","47","46","45","48"],
    //    card: convertCard(card),
    //    hints: [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    //  }))
    //},
    
    hands: {
      self: new Array(5).fill(1).map((_, idx) => ({
        id: schema.cardIds[idx],
        card: convertCard(schema.cheatMyCards[idx]),
        hints: schema.predictions[0][idx]
      })),
      ["player" + schema.partnerId]: schema.cards.map((card, idx) => ({
        id: schema.partnerCardIds[idx],
        card: convertCard(card),
        hints: schema.predictions[1][idx]
      }))
    },
    placed: Object.fromEntries(
      new Map(
        new Array(5)
          .fill(1)
          .map((_, idx) => [schema.colors[idx], schema.piles[idx]])
      )
    ),
    deckComposition: schema.deckComposition,
    hintsLog: schema.history,
    defuseCounter: schema.mulligansRemaining,
    hintCounter: schema.hintStonesRemaining,
    cardsLeft: schema.cardsRemainingInDeck,
    gameOver: false,
    selfId: 0,
    partnerId: 1,
    botName: schema.botName,
    otherBots: schema.otherBots,
    seed: schema.seed,
    history: schema.moveHistory
  };
}
