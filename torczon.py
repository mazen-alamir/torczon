import numpy as np

# This is a simple implementation of a modified version of the torczon 
# derivative free optimization algorithm. 


def improve_S(S=[],  device_f=[]):

    # S is a matrix of dimension (n+1)x(n)
    # each line is a argument values
    # compute the best and make it the first

    y = np.asarray([device_f(S[i, :]) for i in range(S.shape[0])])
    i = np.argmin(y)
    if i > 0:
        S[[i, 0]] = S[[0, i]]

    D = np.asarray([S[0, :]-S[i, :]
                    for i in range(S.shape[0])])

    Sc = S+0.5*D
    Sr = S+2*D
    Se = S+4*D

    yr = np.asarray([device_f(Sr[i, :]) for i in range(S.shape[0])]).min()

    if yr < y[i]:
        ye = np.asarray([device_f(Se[i, :]) for i in range(S.shape[0])]).min()
        if ye < yr:
            Snew = Se
            ynew = ye
        else:
            Snew = Sr
            ynew = yr
    else:
        Snew = Sc
        ynew = y[i]

    return Snew, y[i], ynew


def solve(f_user=[], par=[], x0=[], xmin=[], 
          xmax=[], Nguess=[], Niter=[], initial_box_width=0.1):

    best_y = 1e19
    n = len(xmin)

    def f(x):
        cond1 = np.all([x[i] <= xmax[i] for i in range(n)])
        cond2 = np.all([x[i] >= xmin[i] for i in range(n)])
        if cond1 & cond2:
            return f_user(x,  par)
        else:
            return 2e19

    for ir in range(Nguess):

        if (len(x0) > 0) and (ir == 0):
            S = np.zeros((n+1, n))
            S[0, :] = x0
            for ix in range(n):
                S[ix+1, :] = x0
                S[ix+1, ix] = x0[ix]+initial_box_width
        else:
            Xmin = np.asarray([xmin for i in range(n+1)])
            Xmax = np.asarray([xmax for i in range(n+1)])
            S = Xmin + np.random.rand(n+1, n)*(Xmax-Xmin)
        for i in range(Niter):
            S, y, ynew = improve_S(S=S, device_f=f)
            if ynew < best_y:
                best_y = ynew
                best_x = S[0, :]

        class R:
            pass
        R.f, R.x = best_y, best_x
    return R


if __name__ == '__main__':


    class Data():
        
        def __init__(self):
            self.a = 10
            self.b = -1
            self.c = 0.0
    
    p = Data()

    def fdex(x, p):
        return (x[0]-p.a)**2 +p.c*(x[1]*x[0])**4+(x[1]-p.b)**2

    Nguess = 5
    Niter = 30
    R = solve(fdex, p, [0.0,0.0], [-10,-10], [10, 10], Nguess, Niter)
    print(R.x)

    
