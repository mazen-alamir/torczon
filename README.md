# A simple python implementation of Torczon algorithm

Torczon algorithm is a derivative free algorithm initially designed for unconstrained nonlinear optimization problems. 
Torczon algorithm is a version of the simplex algorithm (not that used in Linear Programming problems) which avoids the 
Collapse of the polygone of solutions that is iteratively updated through the iterations.

This is a modified version of the Torczon algorithm that incorporates:

- Explicitly handling of hard box constraints on the decision variables
- Penalty-based handling of other (non box-like) constraints
- mutiple initial guess option for global optimization.

The main appealing feature of this family of algorithm lies in the fact that the cost function and the constraints need 
not to be differentiable. The counterpart is that this algorithm is not fitted to very high dimensional problems. 

I personally use it intensively in solving real-life problems arising in **Parameterized Nonlinear Model Predictive Control** 
problems. 

## Required packages

- numpy 

## Usage
 
- Define the cost function to be optimized, the cost might embed soft constraint definition via constraint penalty (the penalty can be a part of the variable p that can be any python object or variable. 

```python
def f(x,p):
    
    return ..
```

- Call the solver using 

```python
solve(f_user=f, 
      par=p, x0=x0, 
      xmin=xmin,
      xmax=xmax, 
      Nguess=Nguess, 
      Niter=Niter, 
      initial_box_width=0.1)
```
where 

- **x0**
the initial guess (for the first guess)

- **xmin, xmax** 
the box of admissible values

- **Niter**: 
the number of iterations by single guess 

- **Nguess**: 
the number of initial guesses (randomly sampled using uniform distribution inside the hypercube defined by xmin and xmax)

- **initial_box_width**: 
the amplitude of the initial steps around each initial guess to bild the polygone of the torczon algorithm. 
