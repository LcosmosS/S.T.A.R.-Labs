from optuna.integration import ResourceMonitorCallback


resource_callback = ResourceMonitorCallback(poll_interval=5)  # check memory every 5 sec


study_rf.optimize(objective_rf, n_trials=50, callbacks=[resource_callback])
