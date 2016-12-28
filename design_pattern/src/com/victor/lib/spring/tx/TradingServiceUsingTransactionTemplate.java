package com.victor.lib.spring.tx;


import com.victor.lib.spring.tx.model.TradeOrderData;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.TransactionCallback;
import org.springframework.transaction.support.TransactionTemplate;

/**
 * programmatic transaction scenarios:
 * 1. client-initiated transactions, client launch several RPCs
 * 2. localized JTA transactions, since JTA consumes a lot of resource, use programmatic way to control boundary of transaction can give better performance
 * 3. long-running transactions, one transaction across several sever requests
 */
public class TradingServiceUsingTransactionTemplate {

    private TransactionTemplate transactionTemplate;

    /**
     * in this way, Step1 and Step2 are grouped into one transaction
     * no longer to manually manage connection like:
     * conn.setAutoCommit(false);
     * orderDao.updateTradeOrderStep1(order, conn);
     * orderDao.updateTradeOrderStep2(order, conn);
     * conn.commit();
     * conn.rollback();
     */
    public void updateTradeOrder(TradeOrderData order) throws Exception {
        transactionTemplate.execute(new TransactionCallback() {
            public Object doInTransaction(TransactionStatus status){
                try {
                    TradeOrderDAO dao = new TradeOrderDAO();
                    dao.updateTradeOrderStep1(order);
                    dao.updateTradeOrderStep2(order);
                } catch (Exception e) {
                    status.setRollbackOnly();
                    throw e;
                }
                return null;
            }
        });
    }

    public void setTransactionTemplate(TransactionTemplate transactionTemplate) {
        this.transactionTemplate = transactionTemplate;
    }
}
