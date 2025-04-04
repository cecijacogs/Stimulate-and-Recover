# Simulate-and-Recover
## Project assist using AI

We used a simulate and recover program to analyze the EZ diffusion model. In this experiment, we used an increase of sample size to analyze the following variables. We utilize both mean squared errors (MSE) and mean biases to interpret our results:

    - Boundary Separation (a)
    - Drift Rate (v)
    - Non-decision time (t)

After running the 3000-iteration simulation, there were multiple trends in our dataset. A negative bias was present for both boundary separation (a) and drift rate (v). Both were around -0.05, which suggests an underestimation of these values during the recovery process. To be more exact, the model would underestimate their real value by five percent. This means that the model consistently underestimated these components and approximated their values to be of lower value. The systematic bias seen in boundary separation and drift rate may be caused due to the way they affect each other. For example, if one parameter underestimates a value, it may use the other to compensate for it. 

In comparison to boundary separation and drift rate, non-decision time (t) was far more precise. It was able to recover the parameters with more accuracy, which is indicated by its lower MSE value of less than 0.0025. This means that the model can identify small differences in non-decision time, which can be helpful in experiments and data analyzation. The consistency observed may be due to its role in the model. The way the parameter is structured may indicate that it’s more identifiable, as response times are affected by non-decision time in a more direct way.

Lastly, in contradiction to the hypothesis, there was a lack of improvement in recovery as the sample size increased. Parameter recovery and accuracy did not get better, which we can conclude using both bias and MSE. This observation implies that more data wouldn’t lead to better parameter estimates. This finding is very odd, and can hint at a computational problem in the model. It’s common knowledge that larger sample sizes are better in research. In this case specifically, a larger sample size should’ve provided more reliability in parameter estimation. This trend could be explained by the model itself or in the recovery method. Perhaps there are better approaches to implementing the model in a coding format. If this project were done again, more refinement in the code could lead to better results and accuracy.

To summarize our analysis, the EZ diffusion model is a sound tool in parameter recovery, but it has several flaws and limitations. Due to the negative bias observed in boundary separation and drift rate, it’s important to be cautious when reading results from real datasets. This isn’t to say that the model is bad, as the consistency observed in non-decision time proves some validity. Additionally, perhaps some refinement is needed, as the increase of sample size didn’t improve the model’s accuracy. For future implementations, be mindful of methods to account for this.
