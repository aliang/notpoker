dirname = '/Users/Zach/Desktop/MasterChef1/';

file_list = ls(dirname);
white_space = find(file_list == char(10));
file_names = cell(length(white_space),1);
for i = 1:length(white_space)
    if i == 1
        file_names{i} = file_list(1:white_space(i)-1);
    else
        file_names{i} = file_list(white_space(i-1)+1:white_space(i)-1);
    end
end

nonzero_names = cell(0,1);
for i = 1:size(file_names,1)
    if size(file_names{i},2) > 0
        nonzero_names = [nonzero_names; file_names(i)];
    end
end
file_names = nonzero_names;

file_names = sort(file_names);
used_files = cell(size(file_names,1)/2,1);
for i = 1:size(file_names,1)/2
    used_files(i) = file_names(2*i);
end
file_names = used_files;
winner_array = zeros(length(file_names),1);
num_hands = zeros(length(file_names),1);

for i = 1:length(file_names)
    
    the_file = [dirname file_names{i}];   
    fid = fopen(the_file);
    score = zeros(0,2);
    while 1
        s = fgetl(fid);
        if ~ischar(s)
            break
        elseif findstr(s,'Seat 1:')
            par_open = findstr(s,'(');
            par_close = findstr(s,')');
            score1 = str2double(s(par_open(end)+1:par_close(end)-1));
            t = fgetl(fid);
            par_open = findstr(t,'(');
            par_close = findstr(t,')');
            score2 = str2double(t(par_open(end)+1:par_close(end)-1));
            score = [score; score1 score2];
        end
    end
    fclose(fid);
    
    figure(1);
    clf;
    hold on;
    plot(score(:,1),'b');
    plot(score(:,2),'r');
    legend('n00b','Master Chef',2);
    xlabel('Hands');
    
    if score(end,2) > score(end,1)
        winner_array(i) = 1;
    end
    num_hands(i) = size(score,1);

    pause(0.01);
    
end

avg_win = 100*mean(winner_array)
std_win = 100*sqrt(mean(winner_array)*(1-mean(winner_array))/length(winner_array))
avg_hands = mean(num_hands)

