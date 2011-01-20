clear all
botname = 'masterchef';
dirname = '';
file_list = dir();
badfiles=[];
for i=1:length(file_list)
    if length(file_list(i).name)<4 || ~strcmp(file_list(i).name(end-3:end),'.txt')
        badfiles=[badfiles i];
    end
end
file_list(badfiles)=[];

victory = 0;
defeat = 0;


for i = 1:length(file_list)
    
    the_file = [dirname file_list(i).name];   
    fid = fopen(the_file);
    flag = 2;
    while flag > 0
        s = fgetl(fid);
        if ~isempty(s)
            if s(end) == '*'
                flag = flag - 1;
            elseif strcmp(s(end),'!')
                if s(1:length(botname)) == botname  % ALL HAIL VIVEKBOT
                    victory = victory + 1;
                else
                    defeat = defeat + 1;
                end
            end   
        end
    end
    fclose(fid);
    
end

f = victory/(victory+defeat);
avg_win = 100*f
std_win = 100*sqrt(f*(1-f)/(victory+defeat))

