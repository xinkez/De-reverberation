import pdb

import numpy as np
import scipy as sc
import scipy.io as scio

# import matplotlib.pyplot as plt

import os
from glob import glob
import sys
import multiprocessing as mp

from pre_processing import PreProcessor as Pre
import show_IV_image as showIV
from train_nn import NNTrainer

if __name__ == '__main__':
    DIR_DATA = '../../De-Reverberation Data'
    DIR_WAVFILE = DIR_DATA + '/speech/data/lisa/data/timit/raw/TIMIT/TRAIN'
    DIR_IV = DIR_DATA + '/IV'
    DIR_TRAIN = DIR_IV + '/TRAIN'
    DIR_TEST = DIR_IV + '/TEST'
    FORM = '%04d_%02d.npy'
    ID = '*_converted.wav'

    for arg in sys.argv[1:]:
        if arg.startswith('pre_processing'):
            # N_CORES
            N_CORES = mp.cpu_count()
            try:
                N_CORES *= float(arg.split()[1])
            except IndexError:
                N_CORES *= 0.5
            N_CORES = int(N_CORES)

            # RIR Data
            RIR = scio.loadmat(os.path.join(DIR_DATA, 'RIR.mat'),
                               variable_names='RIR')['RIR']
            RIR = RIR.transpose((2, 0, 1))  # 72 x 32 x 48k

            # SFT Data
            sph_mat = scio.loadmat(os.path.join(DIR_DATA, 'sph_data.mat'),
                                   variable_names=['bEQspec', 'Yenc', 'Ys',
                                                   'Wnv', 'Wpv', 'Vv'])
            bEQspec = sph_mat['bEQspec'].T
            Yenc = sph_mat['Yenc'].T

            Ys_original = np.squeeze(sph_mat['Ys'])
            Ys = np.zeros((Ys_original.size, Ys_original[0].size),
                             dtype=complex)
            for ii in range(Ys_original.size):
                Ys[ii] = np.squeeze(Ys_original[ii])
            del Ys_original

            Wnv = np.array(np.squeeze(sph_mat['Wnv']), dtype=complex)
            Wpv = np.array(np.squeeze(sph_mat['Wpv']), dtype=complex)
            Vv = np.array(np.squeeze(sph_mat['Vv']), dtype=complex)

            del sph_mat

            N_START = len(glob(
                os.path.join(DIR_TRAIN, '*_%02d.npy' % (RIR.shape[0]-1))
            ))+1

            p = Pre(RIR, bEQspec, Yenc, Ys, Wnv, Wpv, Vv)
            p.process(DIR_WAVFILE, ID, N_START, DIR_TRAIN, FORM, N_CORES)

        else:
            metadata = np.load('metadata.npy').item()

            # Fs = metadata['Fs']
            # N_fft = metadata['N_fft']
            # L_frame = metadata['L_frame']
            # L_hop = metadata['L_hop']
            # N_wavfile = metadata['N_wavfile']
            # N_LOC = metadata['N_LOC']

            # del metadata

            if arg.startswith('show_IV_image'):
                FNAME = ''
                arg_sp = arg.split()
                try:
                    FNAME = arg_sp[1]
                    if not FNAME.endswith('.npy'):
                        FNAME += '.npy'
                except IndexError:
                    FNAME = FORM % (1, 0)

                data_dict = np.load(os.path.join(DIR_TRAIN, FNAME)).item()

                showIV.show(data_dict['IV_free'], data_dict['IV_room'],
                            title=[FNAME+' (free)',
                                   FNAME+' (room)'],
                            norm_factor=[data_dict['norm_factor_free'],
                                         data_dict['norm_factor_room']],
                            ylim=[0, metadata['Fs']/2])

            elif arg.startswith('train_nn'):
                del metadata['path_wavfiles']
                trainer = NNTrainer(DIR, DIR_TRAIN, DIR_TEST,
                                    FORM, 'IV_room', 'IV_free',
                                    **metadata)
                trainer.train()

            # elif arg.startswith('histogram'):
            #     IV_free = np.load(FNAME_FREE)
            #     IV_room = np.load(FNAME_ROOM)
            #     bins = 200
            #
            #     plt.figure()
            #     plt.subplot(2,2,1)
            #     plt.hist(IV_free[:,:,:3].reshape(-1), bins=bins)
            #     plt.xlim(IV_free[:,:,:3].min(), IV_free[:,:,:3].max())
            #     plt.title('Histogram for RGB (Free-space)')
            #     plt.subplot(2,2,2)
            #     plt.hist(IV_free[:,:,3].reshape(-1), bins=bins)
            #     plt.xlim(IV_free[:,:,3].min(), IV_free[:,:,3].max())
            #     plt.title('Histogram for alpha (Free-space)')
            #     plt.subplot(2,2,3)
            #     plt.hist(IV_room[:,:,:3].reshape(-1), bins=bins)
            #     plt.xlim(IV_room[:,:,:3].min(), IV_room[:,:,:3].max())
            #     plt.title('Histogram for RGB (Room)')
            #     plt.subplot(2,2,4)
            #     plt.hist(IV_room[:,:,3].reshape(-1), bins=bins)
            #     plt.xlim(IV_room[:,:,3].min(), IV_room[:,:,3].max())
            #     plt.title('Histogram for alpha (Room))')
            #     plt.show()
