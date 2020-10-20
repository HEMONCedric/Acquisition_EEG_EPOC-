
clear classes
addpath_recurse();
CyKITv2 = py.importlib.import_module('CyKITv2');

%iinitiation of Epoc + device
py.CyKITv2.main();

% plotting of gyroscopic values
x=zeros(1,30000);
n=1;
b=[];
    n=0;
    while(n <= 1024) 
        b=[b;cell2mat(cell(py.CyKITv2.get_data()))];
		n
        n=n+1;
    end
eeg_plot(b(:,3:8));
       
%  baseline = 4201.0256409600;


% updates the baseline readings for the sensors
% 
  %if (init_baseline == false),
   %       baseline[select_contact] = (baseline[select_contact] + parseFloat(contact[select_contact]) + 4201.02564096001)/3;
  
  %else
        %  baseline[select_contact] = abs(parseFloat(contact[select_contact]));
  
  %end




