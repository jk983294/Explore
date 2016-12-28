package com.victor.lib.spring.tx.service;

/**
 * one interaction needed between client and server, whole service is dealt in one tx
 * server function manage all tx, so it should set to PROPAGATION_REQUIRED
 */