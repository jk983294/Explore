package com.victor.lib.spring.tx.client;

import com.victor.lib.spring.tx.model.TradeOrderData;

/**
 * the client requires multiple calls to server to fulfill the request.
 * it happens when domain services are too fine-grained and no aggregation services exist.
 * client POJO object use programmatic tx style to manage tx, server side domain service don't manage tx commit or rollback, client side tx context will be passed to server side
 * client function set PROPAGATION_REQUIRED
 * server function set PROPAGATION_MANDATORY
 */
public class ClientModel {

    private TradingService tradingService;

    public void updateTradeOrder(TradeOrderData trade) throws Exception {
        tradingService.updateTradeOrder(trade);
        // other service calls scatter the responsibility
        // so this client object control the tx
    }

    public TradeOrderData getTradeOrder(String key) throws Exception {
        return tradingService.getTrade(key);
    }

    public void setTradingService(TradingService tradingService) {
        this.tradingService = tradingService;
    }
}
