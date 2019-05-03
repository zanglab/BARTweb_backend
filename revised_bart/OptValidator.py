# Time-stamp: <2017-08-10>
'''
Copyright (c) 2017, 2018 Chongzhi Zang, Zhenjia Wang <zhenjia@virginia.edu>

This code is free software; you can redistribute it and/or modify it 
under the terms of the BSD License.

@status: release candidate
@version: $Id$
@author: Chongzhi Zang, Zhenjia Wang
@contact: zhenjia@virginia.edu

'''

import configparser
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

def conf_validate():
    '''
    Read user provided path from 'bart.conf' config file
    '''
    config = configparser.ConfigParser()
    pdir = os.path.dirname
    # config.read(os.path.join(pdir(__file__),'bart.conf'))

    config_path = os.path.join(script_dir, 'bart.conf')
    if not os.path.exists(config_path):
        sys.stderr.write("CRITICAL: bart.conf does not exist in {}!\n".format(script_dir))
        sys.exit(0)

    config.read(config_path)
    return config

def opt_validate(options):
    '''
    Validate input options and specify used data.
    '''
    config = conf_validate()

    if not options.outdir:
        options.outdir = os.path.join(script_dir, 'bart_output')

    if not options.ofilename:
        # input only contains .bam/.bed/.txt
        infilebase = os.path.basename(options.infile)
        if infilebase.endswith('.bam'):
            infilebase = infilebase.split('.bam')[0]
        elif infilebase.endswith('.bed'):
            infilebase = infilebase.split('.bed')[0]
        elif infilebase.endswith('.txt'):
            infilebase = infilebase.split('.txt')[0]
        options.ofilename = os.path.join(options.outdir, infilebase) # xxx(.txt/.bed/.bam)

    # config data path
    # === hg38 ===
    if options.species == 'hg38':   
        if config['path']['hg38_library_dir']:
            data_dir = os.path.join(config['path']['hg38_library_dir'], 'hg38_library')
        else:
            data_dir = os.path.join(script_dir, 'hg38_library')
        print("Library directory:" + data_dir)

        # user for generating cis-regulatory profile
        options.rp = os.path.join(data_dir, 'hg38_RP.h5')
        options.rpkm = os.path.join(data_dir, 'hg38_UDHS_H3K27ac.h5')
        options.tss = os.path.join(data_dir, 'hg38_refseq_TSS.bed')
        options.desc = os.path.join(data_dir, 'SupTable1_HumanH3K27ac_Description.dat')
        options.dhsfile = os.path.join(data_dir, 'hg38_UDHS.bed')

        # used for BART AUC
        options.tffile = os.path.join(data_dir, 'hg38_TF_file.json')
        options.tfoverlap = os.path.join(data_dir, 'hg38_TF_overlap.json')
        if options.subcommand_name == 'geneset':
            options.normfile = os.path.join(data_dir, 'hg38_MSigDB.dat')
        elif options.subcommand_name == 'profile':
            options.normfile = os.path.join(data_dir, 'hg38_H3K27ac.dat')

    # === mm10 ===
    elif options.species == 'mm10': 
        if config['path']['mm10_library_dir']:
            data_dir = os.path.join(config['path']['mm10_library_dir'], 'mm10_library')
        else:
            data_dir = os.path.join(script_dir, 'mm10_library')
        print("Library directory:" + data_dir)

        # user for generating cis-regulatory profile
        options.rp = os.path.join(data_dir, 'mm10_RP.h5')
        options.rpkm = os.path.join(data_dir, 'mm10_UDHS_H3K27ac.h5')
        options.tss = os.path.join(data_dir, 'mm10_refseq_TSS.bed')
        options.desc = os.path.join(data_dir, 'SupTable1_MouseH3K27ac_Description.dat')
        options.dhsfile = os.path.join(data_dir, 'mm10_UDHS.bed')

        # used for BART AUC
        options.tffile = os.path.join(data_dir, 'mm10_TF_file.json')
        options.tfoverlap = os.path.join(data_dir, 'mm10_TF_overlap.json')
        if options.subcommand_name == 'geneset':
            options.normfile = os.path.join(data_dir, 'mm10_H3K27ac.dat')
        elif options.subcommand_name == 'profile':
            options.normfile = os.path.join(data_dir, 'mm10_H3K27ac.dat')

    return options

