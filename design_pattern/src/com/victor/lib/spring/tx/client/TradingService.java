package com.victor.lib.spring.tx.client;


import com.victor.lib.spring.tx.model.TradeOrderData;

public interface TradingService {

    void updateTradeOrder(TradeOrderData trade);

    TradeOrderData getTrade(String key);

    void validateUpdate();
}
