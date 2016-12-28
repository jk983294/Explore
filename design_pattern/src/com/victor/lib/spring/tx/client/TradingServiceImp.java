package com.victor.lib.spring.tx.client;

import com.victor.lib.spring.tx.TradeOrderDAO;
import com.victor.lib.spring.tx.model.TradeOrderData;

public class TradingServiceImp implements TradingService {
    public void updateTradeOrder(TradeOrderData trade){
        validateUpdate();
        TradeOrderDAO dao = new TradeOrderDAO();
        dao.update(trade);
    }

    public TradeOrderData getTrade(String key){
        TradeOrderDAO dao = new TradeOrderDAO();
        return dao.get(key);
    }

    public void validateUpdate(){

    }
}
