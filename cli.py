import argparse
import unittest
from unittest.suite import TestSuite
from run import execute
import subprocess


parser = argparse.ArgumentParser()

parser.add_argument("--fs", help = "filesystem to be mounted")
parser.add_argument("--disk",nargs='+', help = "Name of the disk")
parser.add_argument('--lvname', help="name of the logical volume")
parser.add_argument('--size', help="Determine size of LV")
parser.add_argument('--vgname', help="Enter name of volume group")
args = parser.parse_args()


fs = args.fs
disk_name = args.disk
lvname = args.lvname
size = args.size
vgname = args.vgname

if __name__ == '__main__':
    import test3
    suite = TestSuite()
    loader = unittest.TestLoader()
    
    suite.addTests(loader.loadTestsFromName("test3.Fio"))

    runner = unittest.TextTestRunner()
    runner.run(suite)