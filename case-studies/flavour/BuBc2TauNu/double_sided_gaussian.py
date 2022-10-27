import numpy as np
import tensorflow as tf
import zfit
import zfit.z.numpy as znp

def DSGauss_func(x, mu, sigma_L, sigma_R):
    coef =  znp.sqrt(2.0 / znp.pi) / (sigma_L + sigma_R)
    func = coef * tf.where( tf.less_equal(x, mu), znp.exp(-(x - mu)**2 / sigma_L**2 / 2),  znp.exp(-(x - mu)**2 / sigma_R**2 / 2) )
    return func

def DSGauss_integral(limits, params, model):
    mu = params["mu"]
    sigma_L = params["sigma_L"]
    sigma_R = params["sigma_R"]

    lower, upper = limits._rect_limits_tf

    lower_half = tf.where( tf.less_equal(lower, mu), tf.math.erf( (lower - mu) / sigma_L / tf.math.sqrt(2) ) / 2, tf.math.erf( (lower - mu) / sigma_R / tf.math.sqrt(2) ) / 2 )
    upper_half = tf.where( tf.less_equal(upper, mu), tf.math.erf( (upper - mu) / sigma_L / tf.math.sqrt(2) ) / 2, tf.math.erf( (upper - mu) / sigma_R / tf.math.sqrt(2) ) / 2 )
    return (upper_half - lower_half)


class DSGauss(zfit.pdf.ZPDF):
    _N_OBS = 1
    _PARAMS = ['mu', 'sigma_L', 'sigma_R']

    def _unnormalized_pdf(self, x):
        mu = self.params["mu"]
        sigma_L = self.params["sigma_L"]
        sigma_R = self.params["sigma_R"]
        x = x.unstack_x()

        return DSGauss_func(x=x, mu=mu, sigma_L=sigma_L, sigma_R=sigma_R)


#DSGauss_integral_limits = zfit.Space(axes=(0,), limits=(((zfit.Space.ANY_LOWER,),), ((zfit.Space.ANY_UPPER,),)))

#DSGauss.register_analytic_integral(func=DSGauss_integral, limits=DSGauss_integral_limits)

# Comment out analytic integral
# Error from zfit/core/integration.py 
# AssertionError: Could not integrate, unknown reason. Please fill a bug report.
# Not sure why this happens. Still works without analytic integral, though.  - Xunwu 2022.10.19

