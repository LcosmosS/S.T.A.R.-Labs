# 4. Run MCMC
print("Starting MCMC...")

theta0 = [70.0, 0.300, 0.700, 1e-4, 1e-4]

print("Running Planck 2015 chain...")
pipeline_2015 = JointMCMCPipeline(H_expr, param_names, priors, proposal_widths, joint_2015)
chain_2015 = pipeline_2015.run(theta0=theta0, nsteps=1500)

print("Running Planck 2018 chain...")
pipeline_2018 = JointMCMCPipeline(H_expr, param_names, priors, proposal_widths, joint_2018)
chain_2018 = pipeline_2018.run(theta0=theta0, nsteps=1500)

print("2015:", joint_2015(theta0))
print("2018:", joint_2018(theta0))
print(" Both MCMC chains completed.")