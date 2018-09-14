import os
import subprocess

groupId = 'com.mux'
archiveName = 'exoplayer'

def findFiles(path, ext):
    return [f for f in os.listdir(path) if f.endswith('.' + ext)]

def writePOMfile(path, product, ext):
    x0 = product.find('.' + ext)
    x1 = product.find('-')
    filename = path + '/' + product[:x0] + '.pom'
    with open(filename, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<project xmlns="http://maven.apache.org/POM/4.0.0"\n')
        file.write('   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \n')
        file.write('   xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">\n')
        file.write('   <modelVersion>4.0.0</modelVersion>\n')
        file.write('\n')

        x0 = product.find('-bin.')
        product = product[: x0]
        x0 = product.rfind('-')
        file.write('   <groupId>' + groupId + '</groupId>\n')
        file.write('   <artifactId>' + archiveName + '</artifactId>\n')
        file.write('   <version>' + product[x0 + 1:] + '</version>\n')
        file.write('   <packaging>' + ext + '</packaging>\n')
        file.write('\n')

        product = product[: x0]
        x0 = product.rfind('-')
        file.write('   <name>' + archiveName + '</name>\n')
        file.write('   <description>This is the Mux wrapper around ExoPlayer ' + product[x0 + 1:] + '</description>\n')
        file.write('   <url>https://github.com/muxinc/mux-stats-sdk-exoplayer</url>\n')
        file.write('\n')

        file.write('   <scm>\n')
        file.write('       <connection>scm:git:git@github.com:muxinc/mux-stats-sdk-exoplayer.git</connection>\n')
        file.write('       <developerConnection>scm:git:git@github.com:muxinc/mux-stats-sdk-exoplayer.git</developerConnection>\n')
        file.write('       <url>https://github.com/muxinc/mux-stats-sdk-exoplayer</url>\n')
        file.write('   </scm>\n')
        file.write('\n')

        file.write('   <developers>\n')
        file.write('       <developer>\n')
        file.write('           <name>mux</name>\n')
        file.write('           <email>info@mux.com</email>\n')
        file.write('           <organization>Mux Inc</organization>\n')
        file.write('           <organizationUrl>www.mux.com</organizationUrl>\n')
        file.write('       </developer>\n')
        file.write('   </developers>\n')
        file.write('\n')

        file.write('   <licenses>\n')
        file.write('       <license>\n')
        file.write('           <name>The Apache License, Version 2.0</name>\n')
        file.write('           <url>http://www.apache.org/licenses/LICENSE-2.0.txt</url>\n')
        file.write('       </license>\n')
        file.write('   </licenses>\n')
        file.write('\n')

        file.write('</project>')

def gpgSignProduct(path, product):
    x0 = product.find('-bin.')
    product = product[: x0]
    subprocess.check_output(['gpg','-ab', product + '-bin.aar'])
    subprocess.check_output(['gpg','-ab', product + '-bin.pom'])
    subprocess.check_output(['gpg','-ab', product + '-javadoc.jar'])
    subprocess.check_output(['gpg','-ab', product + '-sources.jar'])


dir_path = os.path.dirname(os.path.realpath(__file__)) + '/MuxExoPlayer/buildout/outputs/publish'
products = findFiles(dir_path, 'aar')
for product in products:
    writePOMfile(dir_path, product, 'aar')

os.chdir(dir_path)
for product in products:
    gpgSignProduct(dir_path, product)