package com.example.khuthon2;

import android.content.Context;
import android.os.Bundle;
import android.widget.Button;

import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferListener;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferNetworkLossHandler;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferObserver;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferState;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferUtility;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.kms.AWSKMS;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.internal.Constants;

import java.io.File;
import java.io.FilterInputStream;

public class AwsConnector {
    private static TransferUtility transferUtility;
    private static File uploadFile;
    private static String downloadFile;
    public static int uploadProgress = 0;
    public static int downloadProgress = 0;

    public static void initializeAwsS3(Context context) {
        CognitoCachingCredentialsProvider credentialsProvider = new CognitoCachingCredentialsProvider(
                context,
                "ap-northeast-2:92d09a73-e234-4439-af7a-6717ca062375",
                Regions.AP_NORTHEAST_2
        );
        AmazonS3 s3 = new AmazonS3Client(credentialsProvider);
        transferUtility = new TransferUtility(s3, context);
        TransferNetworkLossHandler.getInstance(context);

    }

    private class UploadThread extends Thread {

        public void run() {
            TransferObserver observer = transferUtility.upload(
                    "khu-thon",
                    uploadFile.getName(),
                    uploadFile
            );
            observer.setTransferListener(new TransferListener(){
                @Override
                public void onStateChanged(int id, TransferState state) {
                    // do something
                }

                @Override
                public void onProgressChanged(int id, long bytesCurrent, long bytesTotal) {
                    //int percentage = (int) (bytesCurrent/bytesTotal * 100);

                    //System.out.println(percentage);
                }

                @Override
                public void onError(int id, Exception ex) {
                    // do something
                }

            });
        }
    }
    private class DownloadThread extends Thread {
        public void run() {
            TransferObserver observer = transferUtility.download(
                    "khu-thon",
                    downloadFile,
                    new File("/storage/emulated/0/DCIM/Camera/" + downloadFile)
            );
            observer.setTransferListener(new TransferListener(){
                @Override
                public void onStateChanged(int id, TransferState state) {
                    // do something

                }

                @Override
                public void onProgressChanged(int id, long bytesCurrent, long bytesTotal) {
                    int percentage = (int) (bytesCurrent/bytesTotal * 100);

                }

                @Override
                public void onError(int id, Exception ex) {
                    // do something
                }

            });

        }
    }

    public void upload(File f){
        uploadFile = f;

        UploadThread uploadThread = new UploadThread();
        uploadThread.start();
    }

    public void download(String f){
        downloadFile = f;
        DownloadThread downloadThread = new DownloadThread();
        downloadThread.start();
    }
}
