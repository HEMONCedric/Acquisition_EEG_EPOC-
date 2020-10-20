function eeg_plot(X,fs)

if ~exist('fs','var')
   fs=256; 
end

[nPts,n]=size(X);
x=X(:,1);

t=0:1/fs:ceil(length(x)/fs);
t=t(1:length(x));

figure
for i=1:n
    x=X(:,i);
    subplot(n,1,i);
    plot(t,x);title(['eeg signal      fs=', num2str(fs), 'Hz    channel=',num2str(i)]);
end