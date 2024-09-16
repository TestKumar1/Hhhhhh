import os
import subprocess

# Function to install required packages
def install_packages():
    print("Installing required packages...")
    
    # Install Java, Android SDK, and Gradle
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "-y", "openjdk-11-jdk", "gradle", "wget", "unzip"])

    # Download Android Command Line Tools
    if not os.path.exists("commandlinetools-linux.zip"):
        print("Downloading Android SDK Command Line Tools...")
        subprocess.run(["wget", "https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip"])
        subprocess.run(["unzip", "commandlinetools-linux-7583922_latest.zip", "-d", "android-sdk"])
    
    # Set environment variables
    os.environ["ANDROID_HOME"] = os.path.join(os.getcwd(), "android-sdk")
    os.environ["PATH"] += os.pathsep + os.path.join(os.environ["ANDROID_HOME"], "cmdline-tools", "bin")

    # Accept licenses
    subprocess.run([os.path.join(os.environ["ANDROID_HOME"], "cmdline-tools", "bin", "sdkmanager"), "--licenses"])

# Function to create a basic Android project using Gradle
def create_android_project():
    print("Creating Android project...")
    
    # Create project directory
    if not os.path.exists("MyAndroidApp"):
        os.mkdir("MyAndroidApp")

    os.chdir("MyAndroidApp")

    # Create the build.gradle file
    with open("build.gradle", "w") as f:
        f.write("""
plugins {
    id 'com.android.application'
}

android {
    compileSdkVersion 30
    defaultConfig {
        applicationId "com.example.myfirstapp"
        minSdkVersion 15
        targetSdkVersion 30
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.2.0'
    implementation 'com.google.android.material:material:1.2.1'
}
        """)

    # Create a basic directory structure for Android project
    os.makedirs("app/src/main/java/com/example/myfirstapp", exist_ok=True)
    os.makedirs("app/src/main/res/layout", exist_ok=True)
    os.makedirs("app/src/main/res/values", exist_ok=True)

    # Create MainActivity.java
    with open("app/src/main/java/com/example/myfirstapp/MainActivity.java", "w") as f:
        f.write("""
package com.example.myfirstapp;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
        """)

    # Create activity_main.xml layout file
    with open("app/src/main/res/layout/activity_main.xml", "w") as f:
        f.write("""
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello, World!"
        android:textSize="24sp"/>
</LinearLayout>
        """)

    # Create strings.xml file
    with open("app/src/main/res/values/strings.xml", "w") as f:
        f.write("""
<resources>
    <string name="app_name">My First App</string>
</resources>
        """)

    # Create AndroidManifest.xml file
    os.makedirs("app/src/main", exist_ok=True)
    with open("app/src/main/AndroidManifest.xml", "w") as f:
        f.write("""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myfirstapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
        """)

# Function to build the APK
def build_apk():
    print("Building APK...")
    subprocess.run(["gradle", "assembleDebug"])

if __name__ == "__main__":
    install_packages()
    create_android_project()
    build_apk()
