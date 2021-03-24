import fileinput
import logging
import difflib
import glob
import os
import sys

from npb.utils.time import current_time
from npb.utils.files import add_carriage_return
#from npb.utils.files import get_spacecrafts
#from npb.utils.files import get_targets

class PDSLabel(object):

    def __init__(self, setup, product):

        try:
            context_products = product.collection.bundle.context_products
        except:
            context_products = product.bundle.context_products


        #
        # The product to be labeled.
        #
        self.product                    = product
        self.setup                      = setup

        #
        # Fields from setup
        #
        self.root_dir                   = setup.root_dir
        self.mission_accronym           = setup.mission_accronym
        self.XML_MODEL                  = setup.xml_model
        self.SCHEMA_LOCATION            = setup.schema_location
        self.INFORMATION_MODEL_VERSION  = setup.information_model
        self.SPICE_NAME                 = setup.spice_name
        self.PDS4_MISSION_NAME          = setup.mission_name
        self.PDS4_SPACECRAFT_NAME       = setup.spacecraft

        self.CURRENT_YEAR               = current_time().split('-')[0]
        self.BUNDLE_DESCRIPTION_LID     = \
            'urn:nasa:pds:{}.spice:document:spiceds'.format(self.mission_accronym)

        self.PRODUCT_CREATION_TIME      = product.creation_time
        self.PRODUCT_CREATION_DATE      = product.creation_date
        self.FILE_SIZE                  = product.size
        self.FILE_CHECKSUM              = product.checksum

        try:
            self.PDS4_MISSION_LID       = product.collection.bundle.lid_reference
        except:
            self.PDS4_MISSION_LID        = product.bundle.lid_reference

        for context_product in context_products:
            if context_product['name'][0] == setup.spacecraft:
                self.PDS4_SPACECRAFT_TYPE = context_product['type'][0].capitalize()
                self.PDS4_SPACECRAFT_LID  = context_product['lidvid'].split('::')[0]

            #
            # For Bundles with multiple s/c
            #
            if setup.secondary_spacecraft:

                #
                # We sort out how many S/C we have
                #
                sec_scs = setup.secondary_spacecraft.split(',')

                for sc in sec_scs:
                    if sc:
                        if sc.lower() in product.name.lower():
                            self.PDS4_SPACECRAFT_NAME = sc

                            for context_product in context_products:
                                if context_product['name'][0].upper() == sc.upper():
                                    self.PDS4_SPACECRAFT_TYPE = context_product['type'][0].capitalize()
                                    self.PDS4_SPACECRAFT_LID = context_product['lidvid'].split('::')[0]


            self.PDS4_TARGET_NAME = setup.target.upper()

            for context_product in context_products:
                if context_product['name'][0].upper() == setup.target.upper():

                    self.PDS4_TARGET_TYPE = context_product['type'][0].capitalize()
                    self.PDS4_TARGET_LID  = context_product['lidvid'].split('::')[0]

            #
            # For Bundles with multiple targets
            #
            if setup.secondary_target:

                #
                # We sort out how many S/C we have
                #
                sec_tars = setup.secondary_target.split(',')

                for tar in sec_tars:
                    if tar:

                        if tar.lower() in product.name.lower():
                            self.PDS4_TARGET_NAME = tar
                            for context_product in setup.context_products:
                                if context_product['name'][0].upper() == tar.upper():
                                    self.PDS4_TARGET_TYPE = context_product['type'][0].capitalize()
                                    self.PDS4_TARGET_LID = context_product['lidvid'].split('::')[0]

            #
            # For labels that need to include all S/C and Targets of the setup
            #
            self.SPACECRAFTS = self.get_spacecrafts()
            self.TARGETS     = self.get_targets()

        return


    def get_spacecrafts(self):

        sc = ['{}'.format(self.setup.spacecraft)]

        sec_scs = self.setup.secondary_spacecraft.split(',')
        if not isinstance(sec_scs, list):
            sec_scs = [sec_scs]

        scs = sc + sec_scs

        sc_list_for_label = ''

        try:
            context_products = self.product.collection.bundle.context_products
        except:
            context_products = self.product.bundle.context_products


        for sc in scs:
            if sc:
                sc_name = sc.split(',')[0]
                for product in context_products:
                    if product['name'][0] == sc_name and \
                            product['type'][0] == 'Spacecraft':
                        sc_lid = product['lidvid'].split('::')[0]

                sc_list_for_label += \
                    '      <Observing_System_Component>\r\n' + \
                   f'        <name>{sc_name}</name>\r\n' + \
                    '        <type>Spacecraft</type>\r\n' + \
                    '        <Internal_Reference>\r\n' + \
                   f'          <lid_reference>{sc_lid}</lid_reference>\r\n' + \
                    '          <reference_type>is_instrument_host</reference_type>\r\n' + \
                    '        </Internal_Reference>\r\n' + \
                    '      </Observing_System_Component>\r\n'

        sc_list_for_label = sc_list_for_label.rstrip() + '\r\n'

        return sc_list_for_label


    def get_targets(self):

        tar = [self.setup.target]

        sec_tar = self.setup.secondary_target.split(',')
        if not isinstance(sec_tar, list):
            sec_tar = [sec_tar]

        tars = tar + sec_tar

        tar_list_for_label = ''

        try:
            context_products = self.product.collection.bundle.context_products
        except:
            context_products = self.product.bundle.context_products

        for tar in tars:
            if tar:

                target_name = tar
                for product in context_products:
                    if product['name'][0].upper() == target_name.upper():
                        target_lid = product['lidvid'].split('::')[0]
                        target_type = product['type'][0].capitalize()

                tar_list_for_label += \
                    '    <Target_Identification>\r\n' + \
                   f'      <name>{target_name}</name>\r\n' + \
                   f'      <type>{target_type}</type>\r\n' + \
                    '      <Internal_Reference>\r\n' + \
                   f'        <lid_reference>{target_lid}</lid_reference>\r\n' + \
                   f'        <reference_type>{self.get_target_reference_type()}</reference_type>\r\n' + \
                    '      </Internal_Reference>\r\n' + \
                    '    </Target_Identification>\r\n'

        tar_list_for_label = tar_list_for_label.rstrip() + '\r\n'

        return tar_list_for_label


    def get_target_reference_type(self):
        return "data_to_target"


    def write_label(self):

        label_dictionary = vars(self)

        label_extension = '.xml'

        label_name = self.product.path.split('.')[0] + label_extension

        if 'inventory' in label_name:
            label_name = label_name.replace('inventory_','')

        with open(label_name, "w+") as f:

            for line in fileinput.input(self.template):
                line = line.rstrip()
                for key, value in label_dictionary.items():
                    if isinstance(value, str) and key in line and '$' in line:
                        line = line.replace('$'+key, value)

                line = add_carriage_return(line)

                f.write(line)

        self.name = label_name

        logging.info(f'-- Created {label_name}')

        self.validate()

        return


    def validate(self):
        '''
        The label is validated by comparing it to a similar label from the
        previous release of the archive.

        For new archives a 'similar' archive is used.
        :return:
        '''

        logging.info(f'-- Validating  {self.name}')
        logging.info('')

        #
        # 1-Look for a different version of the same file.
        #
        # What we do is that we keep trying to match the label name
        # advancing one character each iteration, in such a way that
        # we find, in order, the label that has the closest name to the
        # one we are generating.
        #
        val_label = ''
        try:

            match_flag = True
            val_label_path = self.setup.final_directory + \
                             f'/{self.setup.mission_accronym}_spice/' + \
                             self.product.collection.name + os.sep

            #
            # If this is the spice_kernels collection, we need to add the
            # kernel type directory.
            #

            if (self.product.collection.name == 'spice_kernels') and  ('collection' not in self.name):
                val_label_path += self.name.split(os.sep)[-2] + os.sep

            val_label_name = self.name.split(os.sep)[-1]
            i = 1

            while match_flag:
                if i < len(val_label_name)-1:
                    val_labels = glob.glob(val_label_path + val_label_name[0:i] + '*.xml')
                    if val_labels:
                        val_labels = sorted(val_labels)
                        val_label = val_labels[-1]
                        match_flag = True
                    else:
                        match_flag = False
                    i += 1

        except:
            pass

        #
        # 2-If a prior version of the same file cannot be found look for
        #   the label of a kernel of the same type.
        #

        #
        # 3-If we cannot find a kernel of the same type; for example is a
        #   first version of an archvie, we compare with an example
        #    label.
        #


        #
        # If a similar label has been found the labels are compared and a
        # diff is being shown in the log. On top of that an HTML file with
        # the comparison is being generated.
        #
        if val_label:

            fromfile = val_label
            tofile   = self.name

            with open(fromfile) as ff:
                fromlines = ff.readlines()
            with open(tofile) as tf:
                tolines = tf.readlines()

            logging.info(f'     Comparing {fromfile.split(os.sep)[-1]} with {tofile.split(os.sep)[-1]}')

            diff = difflib.Differ()
            diff_list = list(diff.compare(fromlines, tolines))
            for line in diff_list:
                if (line[0] == '+') or (line[0] == '-') or (line[0] == '?'):
                    logging.info(line[:-1])
            logging.info('')

            diff = difflib.HtmlDiff().make_file(fromlines, tolines, fromfile, tofile, context=False, numlines=False)
            diff_html = open(self.setup.working_directory + \
                             f"/diff_{fromfile.split(os.sep)[-1].split('.')[0]}_{tofile.split(os.sep)[-1].split('.')[0]}.html", "w")
            diff_html.writelines(diff)
            diff_html.close()

        logging.info('')
        if self.setup.interactive:
            input(">> Press enter to continue...")

        return


class BundlePDS4Label(PDSLabel):

    def __init__(self, setup, readme):

        PDSLabel.__init__(self, setup, readme)

        self.template = self.root_dir + \
                        '/etc/template_bundle.xml'

        self.BUNDLE_LID = self.product.bundle.lid
        self.BUNDLE_VID = self.product.bundle.vid

        self.START_TIME = setup.mission_start
        self.STOP_TIME = setup.increment_stop
        self.FILE_NAME = readme.name
        self.CURRENT_TIME = current_time()
        self.CURRENT_DATE =self.CURRENT_TIME.split('T')[0]
        self.DOI = '' #setup.doi


        for collection in self.product.bundle.collections:
            if collection.name == 'spice_kernels':
                self.SPICE_COLL_LIDVID =  collection.lid + '::' + collection.vid
                self.SPICE_COLL_STATUS = 'Primary'
            if collection.name == 'document':
                self.DOC_COLL_LIDVID =  collection.lid + '::' + collection.vid
                self.DOC_COLL_STATUS = 'Primary'

        self.write_label()

        return

    def get_target_reference_type(self):
        return "bundle_to_target"


class SpiceKernelPDS4Label(PDSLabel):

    def __init__(self, mission, product):

        PDSLabel.__init__(self, mission, product)

        self.template = self.root_dir + \
                        '/etc/template_product_spice_kernel.xml'

        #
        # Fields from Kernels
        #
        self.FILE_NAME = product.name
        self.PRODUCT_LID = self.product.lid
        self.FILE_FORMAT = product.file_format
        self.START_TIME = product.start_time
        self.STOP_TIME = product.stop_time
        self.KERNEL_TYPE_ID = product.type.upper()
        self.PRODUCT_VID = self.product.vid
        self.SPICE_KERNEL_DESCRIPTION = product.description


        extension = '.xml'
        self.name = product.name.split('.')[0] + extension

        self.write_label()

        return


class MetaKernelPDS4Label(PDSLabel):

    def __init__(self, setup, product):

        PDSLabel.__init__(self, setup, product)

        self.template = self.root_dir + '/etc/template_product_spice_kernel_mk.xml'

        #
        # Fields from Kernels
        #
        self.FILE_NAME = product.name
        self.PRODUCT_LID = self.product.lid
        self.FILE_FORMAT = 'Character'
        self.START_TIME = product.start_time
        self.STOP_TIME = product.stop_time
        self.KERNEL_TYPE_ID = product.type.upper()
        self.PRODUCT_VID = self.product.vid
        self.SPICE_KERNEL_DESCRIPTION = product.description

        self.KERNEL_INTERNAL_REFERENCES = self.get_kernel_internal_references()

        self.name = product.name.split('.')[0] + '.xml'

        self.write_label()

        return


    def get_kernel_internal_references(self):

        #
        # From the collection we only use kernels in the MK
        #
        kernel_list_for_label = ''
        for kernel in self.product.collection_metakernel:

            kernel_list_for_label += \
            '    <Internal_Reference>\r\n' + \
            '      <lid_reference>{}\r\n'.format(kernel.lid) + \
            '      </lid_reference>\r\n' + \
            '      <reference_type>data_to_associate</reference_type>\r\n' +\
            '    </Internal_Reference>\r\n'

        kernel_list_for_label = kernel_list_for_label.rstrip() + '\r\n'

        return kernel_list_for_label


class InventoryPDS4Label(PDSLabel):

    def __init__(self, setup, collection, inventory):

        PDSLabel.__init__(self, setup, inventory)

        self.collection = collection
        self.template = self.root_dir + \
                        '/etc/template_collection_{}.xml'.format(collection.type)

        self.COLLECTION_LID = self.collection.lid
        self.COLLECTION_VID = self.collection.vid
        self.START_TIME = setup.mission_start
        self.STOP_TIME = setup.increment_stop
        self.FILE_NAME = inventory.name

        # Count number of lines in the inventory file
        f = open(self.product.path)
        self.N_RECORDS = str(len(f.readlines()))
        f.close()

        self.name = collection.name.split('.')[0] + '.xml'

        self.write_label()

        return


    def get_target_reference_type(self):
        return "collection_to_target"


class InventoryPDS3Label(PDSLabel):

    def __init__(self, setup, collection, inventory):

        PDSLabel.__init__(self, setup, inventory)

        self.collection = collection
        self.template = self.root_dir + \
                        '/etc/template_collection_{}.LBL'.format(
                            collection.type)

        self.VOLUME = setup.volume
        self.PRODUCT_CREATION_TIME = current_time()
        self.DATASET = setup.dataset

        indexfile = open(setup.bundle_directory + '/INDEX/INDEX.TAB', 'r').readlines()
        self.N_RECORDS = str(len(indexfile))
        self.R_RECORDS = str(len(indexfile[0]) + 1)
        indexfields = indexfile[0].replace('"', '').split(',')
        self.START_BYTE1 = str(2)
        self.START_BYTE2 = str(2 + len(indexfields[0]) + 3)
        self.START_BYTE3 = str(2 + len(indexfields[0]) + 3 + len(indexfields[1]) + 2)
        self.START_BYTE4 = str(2 + len(indexfields[0]) + 3 + len(indexfields[1]) + 2 + len(indexfields[2]) + 2)
        self.BYTES1 = str(len(indexfields[0]))
        self.BYTES2 = str(len(indexfields[1]))
        self.BYTES3 = str(len(indexfields[2]))
        self.BYTES4 = str(len(indexfields[3].split('\n')[0]))

        self.write_label()

        return


    def write_label(self):

        label_dictionary = vars(self)


        with open(self.setup.bundle_directory + '/INDEX/INDEX.LBL', "w+") as f:

            for line in fileinput.input(self.template):
                line = line.rstrip()
                for key, value in label_dictionary.items():
                    if isinstance(value, str) and key in line and '$' in line:
                        line = line.replace('$' + key, value)

                line = add_carriage_return(line)

                if 'END_OBJECT' in line and line[:10] != 'END_OBJECT':
                    f.write(line.split('END_OBJECT')[0])
                    f.write('END_OBJECT               = COLUMN\n')
                else:
                    f.write(line)

        self.name = 'INDEX.LBL'

        return


class DocumentPDS4Label(PDSLabel):

    def __init__(self, setup, collection, inventory):

        PDSLabel.__init__(self, setup, inventory)

        self.setup = setup
        self.collection = collection
        self.template = self.root_dir + \
                        '/etc/template_product_html_document.xml'

        self.PRODUCT_LID = inventory.lid
        self.PRODUCT_VID = inventory.vid
        self.START_TIME = setup.mission_start
        self.STOP_TIME = setup.mission_stop
        self.FILE_NAME = inventory.name
        self.CURRENT_TIME = current_time()
        self.CURRENT_DATE =self.CURRENT_TIME.split('T')[0]

        self.name = collection.name.split('.')[0] + '.xml'

        self.write_label()

        return