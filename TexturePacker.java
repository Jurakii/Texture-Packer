import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.IOException;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;
import javax.imageio.ImageIO;
import javax.swing.*;

public class TexturePacker extends JFrame {

    private static final long serialVersionUID = 1L;

    private JComboBox<String> sourcePathsCombobox;
    private JComboBox<String> destinationPathsCombobox;
    private JButton compressButton;
    private JProgressBar progressBar;

    public TexturePacker() {
        setTitle("Texture Packer");
        setSize(425, 350);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new GridBagLayout());

        JLabel sourceLabel = new JLabel("Source Folder:");
        JLabel destinationLabel = new JLabel("Destination Folder:");
        sourcePathsCombobox = new JComboBox<>(new String[]{"Select a source folder"});
        destinationPathsCombobox = new JComboBox<>(new String[]{"Select a destination folder"});

        JButton newButton = new JButton("New Source");
        newButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addFilePath(sourcePathsCombobox);
            }
        });

        JButton newButton2 = new JButton("New Destination");
        newButton2.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addFilePath(destinationPathsCombobox);
            }
        });

        compressButton = new JButton("Save and Compress");
        compressButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                setDestinationAndCompress();
            }
        });

        progressBar = new JProgressBar(0, 100);

        GridBagConstraints constraints = new GridBagConstraints();
        constraints.fill = GridBagConstraints.HORIZONTAL;
        constraints.weightx = 1;
        constraints.gridx = 0;
        constraints.gridy = 0;
        constraints.insets = new Insets(10, 10, 10, 10);  // Add top and bottom margins
        add(newButton, constraints);

        constraints.gridx = 1;
        add(newButton2, constraints);

        constraints.gridy = 1;
        constraints.gridx = 0;
        add(sourceLabel, constraints);

        constraints.gridx = 1;
        add(destinationLabel, constraints);

        constraints.gridy = 2;
        constraints.gridwidth = 1;
        add(destinationPathsCombobox, constraints);

        constraints.gridx = 0;
        add(sourcePathsCombobox, constraints);

        constraints.gridwidth = 2;
        constraints.gridy = 3;
        constraints.insets = new Insets(20, 10, 0, 10);  // Add only bottom margin
        add(compressButton, constraints);

        constraints.gridy = 4;
        add(progressBar, constraints);

try {
    InputStream iconStream = TexturePacker.class.getResourceAsStream("/icon.png");
    if (iconStream != null) {
        Image icon = ImageIO.read(iconStream);
        setIconImage(icon);
    } else {
        System.err.println("Icon not found");
    }
} catch (IOException e) {
    e.printStackTrace(); // Handle exception appropriately
}

        setVisible(true);
    }

    private void addFilePath(JComboBox<String> combobox) {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFolder = fileChooser.getSelectedFile();
            combobox.addItem(selectedFolder.getPath());
        }
    }

    private void setDestinationAndCompress() {
        String selectedFolderValue = (String) sourcePathsCombobox.getSelectedItem();
        String selectedDestinationValue = (String) destinationPathsCombobox.getSelectedItem();
        if (selectedFolderValue != null && selectedDestinationValue != null) {
            String zipFilename = selectedDestinationValue + File.separator + "Textures.zip";
            compressButton.setEnabled(false);
            new Thread(() -> compressFolder(selectedFolderValue, selectedDestinationValue, zipFilename)).start();
        }
    }

    private void compressFolder(String sourceFolder, String destinationFolder, String zipFilename) {
        try {
            AtomicInteger progress = new AtomicInteger(0);
            File source = new File(sourceFolder);
            int totalFiles = countFiles(source);
            SwingUtilities.invokeLater(() -> progressBar.setMaximum(totalFiles));

            try (ZipOutputStream zipOutputStream = new ZipOutputStream(new FileOutputStream(zipFilename))) {
                compress(source, source, zipOutputStream, progress);
            }

            SwingUtilities.invokeLater(() -> JOptionPane.showMessageDialog(this, "Successfully compressed files to " + zipFilename));
        } catch (Exception e) {
            SwingUtilities.invokeLater(() -> JOptionPane.showMessageDialog(this, "Error: " + e.getMessage()));
        } finally {
            SwingUtilities.invokeLater(() -> compressButton.setEnabled(true));
        }
    }

    private void compress(File root, File sourceFolder, ZipOutputStream zipOutputStream, AtomicInteger progress) throws IOException {
        for (File file : sourceFolder.listFiles()) {
            if (file.isDirectory()) {
                compress(root, file, zipOutputStream, progress);
            } else {
                String relativePath = root.toURI().relativize(file.toURI()).getPath();
                ZipEntry zipEntry = new ZipEntry(relativePath);
                zipOutputStream.putNextEntry(zipEntry);
                byte[] bytes = new byte[1024];
                int length;
                while ((length = ImageIO.createImageInputStream(file).read(bytes)) >= 0) {
                    zipOutputStream.write(bytes, 0, length);
                }
                zipOutputStream.closeEntry();
                progress.incrementAndGet();
                SwingUtilities.invokeLater(() -> progressBar.setValue(progress.get()));
            }
        }
    }

    private int countFiles(File file) {
        if (file.isFile()) {
            return 1;
        }
        int count = 0;
        for (File child : file.listFiles()) {
            count += countFiles(child);
        }
        return count;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new TexturePacker());
    }
}
