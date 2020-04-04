function main(params) {
    /* default to double function! */
    console.log (params)
    let step = params.step || 0
    delete params.step
    switch (step) {
        case 0: return { action: 'double', params, state: { step: 3  }  }
        case 1: return { action: 'triple', params, state: { step: 3  }  }
        case 2: return { action: 'quadruple', params, state: { step: 3  }  }
        case 3: return { action: 'increment', params, state: { step: 4  }  }
        case 4: return { params  }
    }
}
