function addpath_recurse()
    delete(py.sys.path);
	%% A changer en fonction de l'adresse ou se trouve le répertoire téléchargé
    root_path = 'C:\Users\Asus\Downloads\Python\'; 
    insert(py.sys.path,int32(0),'');
    insert(py.sys.path,int32(0),[root_path 'cyUSB']);
end 
