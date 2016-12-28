package com.victor.lib.spring.tx;

import com.victor.lib.spring.tx.model.TradeOrderData;

public class TradingServiceBean {

    /**
     * declarative transaction way
     */
    public void updateTradeOrder(TradeOrderData order) throws Exception {
        TradeOrderDAO dao = new TradeOrderDAO();
        dao.updateTradeOrderStep1(order);
        dao.updateTradeOrderStep2(order);
    }
}
