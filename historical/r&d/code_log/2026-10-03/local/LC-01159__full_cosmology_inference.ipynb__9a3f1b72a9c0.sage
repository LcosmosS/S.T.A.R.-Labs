# 4. Run MCMC for both Planck datasets

pipeline_2015 = JointMCMCPipeline(H_expr, param_names, priors, proposal_widths, joint_2015)
chain_2015 = pipeline_2015.run(theta0=[70, 0.3, 0.7, 0, 0], nsteps=8000)
