package com.victor.lib.spring.tx;

/**
 * Transaction Attributes:
 *
 * PROPAGATION_REQUIRED, use existing tx-context, if no existing one, create one
 *
 * PROPAGATION_MANDATORY, must have existing tx-context, if not exist, throw TransactionRequiredException
 * best practice: if the method needs a tx, but not correspond to set rollback state
 *
 * PROPAGATION_REQUIRES_NEW,suspend existing outside tx, always create a new tx
 * typical application: log must require new tx to record action no matter outside business logic is committed successfully
 *
 * PROPAGATION_SUPPORTS, it there happen a tx ctx there, this method will use that
 * typical application: read operation can be executed without ctx, but when this read embedded in ctx, then it will see the updates of this ctx
 * like: read stock count, initial value is 10m, then add 1m, then read it is 11m, if we don't use PROPAGATION_SUPPORTS, we will always see 10m until committed.
 *
 * PROPAGATION_NOT_SUPPORTED, it will suspend current existing tx, and resume it after this method finished
 * typical application: bypass the sproc contains DDL statements, it will cause exception in XA tx
 *
 * PROPAGATION_NEVER, throw exception when tx founded
 */


/**
 * Isolation level go up, concurrency level go down and consistency level go up
 * Uncommitted Read, it can read other tx's uncommitted write data, if other tx rollback, then this value is dirty value for current tx
 * Committed Read, if other tx is changing data, this data is not available for current tx until other tx commit
 * RepeatableRead, if read several times in current tx, it will get exactly the same result set, it means it will block other tx's write operation
 * Serializable, only one tx can access the data
 */

/**
 * The two-phase commit protocol (2PC)
 * phase one: ask all resources are ready, they can response (READY, READ_ONLY, NOT_READY), if any NOT_READY received, rollback
 * phase two: all resources commit, "READ_ONLY" resource will be ignored
 *
 * XA protocol use 2PC
 *
 * HeuristicRollbackException in commit phase, all resources decide to rollback
 * HeuristicMixedException in commit phase, some resources decide to rollback while some decide to commit
 *
 * XAResource interface for all resources need TA support
 */

/**
 * Transaction Design Pattern
 *
 * Client Owner Transaction Design Pattern
 *
 *
 * Domain Service Owner Transaction Design Pattern
 * one interaction needed between client and server, whole service is dealt in one tx
 *
 * Server Delegate Owner Transaction Design Pattern
 *
 */