profile_images

product_images

python3 -m venv venv
source venv/bin/activate      
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Install required dependencies
sudo apt update
sudo apt install -y python3-pip build-essential git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install Buildozer
pip3 install --user buildozer
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Install Cython
pip3 install --user Cython==0.29.19
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
[app]

# Application title
title = HTF Marketplace

# Package name
package.name = htfmarket

# Package domain (reverse DNS format)
package.domain = org.htf

# Source directory
source.dir = .

# Source file to run
source.include_exts = py,png,jpg,jpeg
main.py = new-1.py

# Application version
version = 1.0

# Requirements
requirements = python3, pygame, kivy, android

# Orientation (landscape for our app)
orientation = landscape

# Android API level
android.api = 33

# Minimum Android SDK version
android.minapi = 21

# Android SDK path (leave empty for auto)
# android.sdk_path = 

# Android NDK path (leave empty for auto)
# android.ndk_path = 

# Set to 1 to enable AndroidX
android.enable_androidx = 1

# Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# Presplash image (optional)
# presplash.filename = %(source.dir)s/presplash.png

# Icon file (optional)
# icon.filename = %(source.dir)s/icon.png

# Extra files to include
source.include_patterns = product_images/*,profile_images/*

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------
