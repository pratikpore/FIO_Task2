from run import execute
import unittest
import cli
from run import execute

class Fio(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        execute("sudo umount /")
        execute("sudo lvremove -ff {}".format(cli.vgname))
        execute("sudo vgremove {}".format(cli.vgname))
        execute("sudo pvremove {}".format(cli.disk_name))
        print("Done")

        
    def test_pvcreate(self):
        execute("sudo pvcreate {}".format(cli.disk_name))
        for i in cli.d:
            self.assertRegex(execute("sudo pvdisplay").stdout, i)

        execute("sudo vgcreate {} {}".format(cli.vgname,cli.disk_name))
        self.assertRegex(execute("sudo vgdisplay").stdout, cli.vgname)

    
        execute("sudo lvcreate -n {} --size {}G {}".format(cli.lvname,cli.lvsize,cli.vgname))
        self.assertRegex(execute("sudo lvdisplay").stdout, cli.lvname)

        print("\n PV  LV  VG has been created")


    def test_fscreate(self):
        execute("sudo pvcreate {}".format(cli.disk_name))
        for i in cli.d:
            self.assertRegex(execute("sudo pvdisplay").stdout, i)
            
        execute("sudo vgcreate {} {}".format(cli.vgname,cli.disk_name))
        self.assertRegex(execute("sudo vgdisplay").stdout, cli.vgname)
        
        execute("sudo lvcreate -n {} --size {}G {}".format(cli.lvname,cli.lvsize,cli.vgname))
        self.assertRegex(execute("sudo lvdisplay").stdout, cli.lvname)

        print("\n PV  LV  VG has been created, \n Creating file system")
        
        
        self.file_dest = "/"
        self.lvpath = ("/dev/{}/{}".format(cli.vgname,cli.lvname))
        execute("sudo mkfs.{} {}".format(cli.fs,self.lvpath))
        execute("mkdir {}".format(self.file_dest))
        execute("mount {} {}".format(self.lvpath,self.file_dest))
        self.assertRegex(execute("df -h").stdout, self.file_dest)
        print("\n File has been created & mounted")

        #def test_checkio(self):
        a = execute("sudo fio --filename={} --size=500GB --direct=1 --rw=randrw --bs=4k --ioengine=libaio --iodepth=256 --runtime=120 --numjobs=4 --time_based --group_reporting --name=iops-test-job --eta-newline=1".format(self.lvpath))
        self.assertRegex(a.stdout, "Run status")
        print("IO has been verified")

        
        #Note-
        #this for xfs file
        #data for ext4 file
