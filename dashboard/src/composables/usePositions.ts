class NotImplementedError extends Error {
  constructor() {
    super("The callback for the following actions was not implemented.")
  }
}

export const usePositions = () => {
  const closeAllPositions = () => {
    const response = confirm("Are you sure you want to close all open positions?")

    if (!response) return

    // TODO: post to trading service
    throw new NotImplementedError()
  }

  return {
    closeAllPositions
  }
}
